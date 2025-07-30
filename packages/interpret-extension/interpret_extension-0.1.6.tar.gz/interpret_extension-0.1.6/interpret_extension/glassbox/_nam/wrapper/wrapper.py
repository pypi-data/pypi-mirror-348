import os
import random
from typing import Callable

import numpy as np
from numpy.typing import ArrayLike
import pandas as pd
import scipy
from sklearn.exceptions import NotFittedError
import torch

from ..._nam.data import NAMDataset
from ..._nam.models import NAM, MultiTaskNAM
from ..._nam.models import get_num_units
from ..._nam.models.saver import Checkpointer
from ..._nam.trainer import Trainer
from ..._nam.trainer.losses import make_penalized_loss_func

from sklearn.base import ClassifierMixin, is_classifier
from sklearn.utils.validation import check_is_fitted
from ....api.base import ExplainerMixin
from ....api.templates import FeatureValueExplanation
from ....utils._clean_simple import clean_dimensions, typify_classification
from ....utils._clean_x import preclean_X
from ....utils._explanation import (
    gen_global_selector,
    gen_local_selector,
    gen_name_from_class,
    gen_perf_dicts,
)
from ....utils._unify_data import unify_data

class NAMBase:
    def __init__(
        self,
        units_multiplier: int = 2,
        num_basis_functions: int = 64,
        hidden_sizes: list = [64, 32],
        dropout: float = 0.1,
        feature_dropout: float = 0.05, 
        batch_size: int = 1024,
        num_workers: int = 0,
        num_epochs: int = 1000,
        log_dir: str = None,
        val_split: float = 0.15,
        device: str = 'cpu',
        lr: float = 0.02082,
        decay_rate: float = 0.0,
        output_reg: float = 0.2078,
        l2_reg: float = 0.0,
        save_model_frequency: int = 10,
        patience: int = 60,
        monitor_loss: bool = True,
        early_stop_mode: str = 'min',
        loss_func: Callable = None,
        metric: str = None,
        num_learners: int = 1,
        n_jobs: int = None,
        warm_start: bool = False,
        random_state: int = 42,
        feature_names: list = None,
        feature_types: list = None
    ) -> None:
        self.units_multiplier = units_multiplier
        self.num_basis_functions = num_basis_functions
        self.hidden_sizes = hidden_sizes
        self.dropout = dropout
        self.feature_dropout = feature_dropout
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.num_epochs = num_epochs
        self.log_dir = log_dir
        self.val_split = val_split
        self.device = device
        self.lr = lr
        self.decay_rate = decay_rate
        self.output_reg = output_reg
        self.l2_reg = l2_reg
        self.save_model_frequency = save_model_frequency
        self.patience = patience
        self.monitor_loss = monitor_loss
        self.early_stop_mode = early_stop_mode
        self.loss_func = loss_func
        self.metric = metric
        self.num_learners = num_learners
        self.n_jobs = n_jobs
        self.warm_start = warm_start
        self.random_state = random_state
        self.feature_names = feature_names
        self.feature_types = feature_types

        self._best_checkpoint_suffix = 'best'
        self._fitted = False

    def _set_random_state(self):
        random.seed(self.random_state)
        np.random.seed(self.random_state)
        torch.manual_seed(self.random_state)
        return
    
    def _initialize_models(self, X, y):
        self.num_tasks = y.shape[1] if len(y.shape) > 1 else 1
        self.num_inputs = X.shape[1]
        self.models = []
        for _ in range(self.num_learners):
            model = NAM(num_inputs=self.num_inputs,
                num_units=get_num_units(self.units_multiplier, self.num_basis_functions, X),
                dropout=self.dropout,
                feature_dropout=self.feature_dropout,
                hidden_sizes=self.hidden_sizes)
            self.models.append(model)

        return

    def _models_to_device(self, device):
        for model in self.models:
            model.to(device)

        return

    def fit(self, X, y, w=None):
        """
        Fits the model.

        Args:
            X: Numpy array for training instances.
            y: Numpy array as training labels.
        """
        y = clean_dimensions(y, "y")
        if y.ndim != 1:
            msg = "y must be 1 dimensional"
            raise ValueError(msg)
        if len(y) == 0:
            msg = "y cannot have 0 samples"
            raise ValueError(msg)
        
        if is_classifier(self):
            y = typify_classification(y)
        else:
            y = y.astype(np.float64, copy=False)

        self._set_random_state()
        if not self.warm_start or not self._fitted:
            self._initialize_models(X, y)

        X, n_samples = preclean_X(X, self.feature_names, self.feature_types, len(y))

        X, self.feature_names_in_, self.feature_types_in_ = unify_data(
            X, n_samples, self.feature_names, self.feature_types, False, 0
        )

        self.X_mins_ = np.min(X, axis=0)
        self.X_maxs_ = np.max(X, axis=0)
        self.categorical_uniq_ = {}

        for i, feature_type in enumerate(self.feature_types_in_):
            if feature_type in ("nominal", "ordinal"):
                self.categorical_uniq_[i] = sorted(set(X[:, i]))

        unique_val_counts = np.zeros(len(self.feature_names_in_), dtype=np.int64)
        for col_idx in range(len(self.feature_names_in_)):
            X_col = X[:, col_idx]
            unique_val_counts[col_idx] = len(np.unique(X_col))

        # to use in the global explanation
        self.global_selector_ = gen_global_selector(
            len(self.feature_names_in_),
            self.feature_names_in_,
            self.feature_types_in_,
            unique_val_counts,
            None,
        )
        self.bin_counts_, self.bin_edges_ = _hist_per_column(X, self.feature_types_in_)

        self.partial_fit(X, y)
        return self

    def partial_fit(self, X, y, w=None) -> None:
        self._models_to_device(self.device)
        
        dataset = NAMDataset(X, y, w)

        self.criterion = make_penalized_loss_func(self.loss_func, 
            self.regression, self.output_reg, self.l2_reg)

        self.trainer = Trainer(
            models=self.models,
            dataset=dataset,
            metric=self.metric,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            num_epochs=self.num_epochs,
            log_dir=self.log_dir,
            val_split=self.val_split,
            test_split=None,
            device=self.device,
            lr=self.lr,
            decay_rate=self.decay_rate,
            save_model_frequency=self.save_model_frequency,
            patience=self.patience,
            monitor_loss=self.monitor_loss,
            early_stop_mode=self.early_stop_mode,
            criterion=self.criterion,
            regression=self.regression,
            num_learners=self.num_learners,
            n_jobs=self.n_jobs,
            random_state=self.random_state
        )
        
        self.trainer.train_ensemble()
        self.trainer.close()

        # Move models to cpu so predictions can be made on cpu data
        self._models_to_device('cpu')

        self._fitted = True
        return self

    def predict(self, X) -> ArrayLike:
        if not self._fitted:
            raise NotFittedError('''This NAM instance is not fitted yet. Call \'fit\' 
                with appropriate arguments before using this method.''')

        if isinstance(X, pd.DataFrame):
            X = X.to_numpy()

        X = torch.tensor(X.astype(np.float32), requires_grad=False, dtype=torch.float)
        predictions = np.zeros((X.shape[0], self.num_tasks))

        for model in self.models:
            preds, _ = model.forward(X)
            predictions += preds.detach().cpu().numpy()

        return predictions / self.num_learners

    def plot(self, feature_index) -> None:
        num_samples = 3000
        X = np.zeros((num_samples, self.num_inputs))
        #X[:, feature_index] = np.linspace(self.X_mins_[feature_index], self.X_maxs_[feature_index], num_samples)
        amplification = 0.1 * (self.X_maxs_[feature_index] - self.X_mins_[feature_index])
        X[:, feature_index] = np.linspace(self.X_mins_[feature_index] - amplification, self.X_maxs_[feature_index] + amplification, num_samples)        
        
        feature_outputs = []
        for model in self.models:
            # (examples, tasks, features)
            _, fnns_out = model.forward(torch.tensor(X, dtype=torch.float32))
            if self.num_tasks == 1:
                fnns_out = fnns_out.unsqueeze(dim=1)
            # (examples, tasks)
            feature_outputs.append(fnns_out[:, :, :, feature_index].detach().cpu().numpy())

        # (learners, examples, tasks)
        feature_outputs = np.stack(feature_outputs, axis=0)
        # (examples, tasks)
        y = np.mean(feature_outputs, axis=0).squeeze()
        conf_int = np.std(feature_outputs, axis=0).squeeze()
        # TODO: Scale conf_int according to units of y

        # X = self._preprocessor.inverse_transform(X)
        
        return {'x': X[:, feature_index], 'y': y, 'conf_int': conf_int}

    def load_checkpoints(self, checkpoint_dir):
        self.models = []
        for i in range(self.num_learners):
            checkpointer = Checkpointer(os.path.join(checkpoint_dir, str(i)))
            model = checkpointer.load(self._best_checkpoint_suffix)
            model.eval()
            self.num_tasks = 1 if isinstance(model, NAM) else model.num_tasks
            self.models.append(model)

        self._fitted = True
        return
    
    def get_contributions(self, X):
        feature_outputs = []

        for m in self.models:
            _, fnns_out = m.forward(torch.tensor(X.astype(np.float32), dtype=torch.float32))
            fnns_out = fnns_out.unsqueeze(dim=1)
            feature_outputs.append(fnns_out[:, :, :, :].detach().cpu().numpy())

        feature_outputs = np.stack(feature_outputs, axis=0)
        y = np.mean(feature_outputs, axis=0).squeeze()
        return y
        
    def explain_local(self, X, y=None, name=None):
        if name is None:
            name = gen_name_from_class(self)

        n_samples = None
        if y is not None:
            y = clean_dimensions(y, "y")
            if y.ndim != 1:
                msg = "y must be 1 dimensional"
                raise ValueError(msg)
            n_samples = len(y)

            if is_classifier(self):
                y = typify_classification(y)
            else:
                y = y.astype(np.float64, copy=False)
        
        X, n_samples = preclean_X(
            X, self.feature_names_in_, self.feature_types_in_, n_samples
        )

        if n_samples == 0:
            msg = "X cannot have 0 samples"
            raise ValueError(msg)
        
        X, _, _ = unify_data(
            X, n_samples, self.feature_names_in_, self.feature_types_in_, False, 0
        )
        
        classes = np.array([0, 1], np.int64)
        is_classification = is_classifier(self)

        predictions = self.predict_proba(X).squeeze()
        individual_preds = self.get_contributions(X)

        intercept = np.mean([m._bias.item() for m in self.models])

        data_dicts = []
        scores_list = []
        perf_list = []
        perf_dicts = gen_perf_dicts(predictions, y, is_classification, classes)
        for i, instance in enumerate(X):
            scores = individual_preds[i, :]
            scores_list.append(scores)
            data_dict = {}
            data_dict["data_type"] = "univariate"

            # Performance related (conditional)
            perf_dict_obj = None if perf_dicts is None else perf_dicts[i]
            data_dict["perf"] = perf_dict_obj
            perf_list.append(perf_dict_obj)

            # Names/scores
            data_dict["names"] = self.feature_names_in_
            data_dict["scores"] = scores

            # Values
            data_dict["values"] = instance

            data_dict["extra"] = {
                "names": ["Intercept"],
                "scores": [intercept],
                "values": [1],
            }

            data_dict["meta"] = {"label_names": classes.tolist()}

            data_dicts.append(data_dict)
        
        internal_obj = {
            "overall": None,
            "specific": data_dicts,
            "mli": [
                {
                    "explanation_type": "local_feature_importance",
                    "value": {
                        "scores": scores_list,
                        "intercept": intercept,
                        "perf": perf_list,
                    },
                }
            ],
        }
        internal_obj["mli"].append(
            {
                "explanation_type": "evaluation_dataset",
                "value": {"dataset": X, "dataset_y": y},
            }
        )

        selector = gen_local_selector(data_dicts, is_classification=is_classification)

        return FeatureValueExplanation(
            "local",
            internal_obj,
            feature_names=self.feature_names_in_,
            feature_types=self.feature_types_in_,
            name=name,
            selector=selector,
        )

    def explain_global(self, name=None):
        check_is_fitted(self)

        if name is None:
            name = gen_name_from_class(self)

        intercept = np.mean([m._bias.item() for m in self.models])

        specific_data_dicts = []
        overall_scores = []
        for index, _ in enumerate(self.feature_names_in_):
            plot = self.plot(index)
            grid_points = plot['x']
            y_scores = plot['y']

            # TODO: Modify overall scores
            overall_scores.append(np.std(y_scores))

            data_dict = {
                "names": grid_points,
                "scores": y_scores,
                "density": {
                    "scores": self.bin_counts_[index],
                    "names": self.bin_edges_[index],
                },
            }

            specific_data_dicts.append(data_dict)

        # TODO: Modify overall scores and intercept
        overall_data_dict = {
            "names": self.feature_names_in_,
            "scores": list(overall_scores),
            "extra": {"names": ["Intercept"], "scores": [intercept]},
        }

        internal_obj = {
            "overall": overall_data_dict,
            "specific": specific_data_dicts,
            "mli": [
                {
                    # TODO: What is this?
                    "explanation_type": "global_feature_importance",
                    "value": {"scores": list(y_scores), "intercept": intercept},
                }
            ],
        }
        return NAMExplanation(
            "global",
            internal_obj,
            feature_names=self.feature_names_in_,
            feature_types=self.feature_types_in_,
            name=name,
            selector=self.global_selector_,
        )

class NAMExplanation(FeatureValueExplanation):
    """Visualizes specifically for NAM methods."""

    explanation_type = None

    def __init__(
        self, 
        explanation_type, 
        internal_obj, 
        feature_names=None, 
        feature_types=None, 
        name=None, 
        selector=None,
    ):
        """Initializes class.
        
        Args:
            explanation_type:  Type of explanation.
            internal_obj: A jsonable object that backs the explanation.
            feature_names: List of feature names.
            feature_types: List of feature types.
            name: User-defined name of explanation.
            selector: A dataframe whose indices correspond to explanation entries.
        """
        super().__init__(
            explanation_type, 
            internal_obj, 
            feature_names, 
            feature_types, 
            name, 
            selector,
        )

    def visualize(self, key=None):
        """Provides interactive visualizations.

        Args:
            key: Either a scalar or list
                that indexes the internal object for sub-plotting.
                If an overall visualization is requested, pass None.

        Returns:
            A Plotly figure.
        """
        from ....visual.plot import (
            get_explanation_index,
            get_sort_indexes,
            mli_plot_horizontal_bar,
            mli_sort_take,
            plot_horizontal_bar,
            sort_take,
        )

        if isinstance(key, tuple) and len(key) == 2:
            provider, key = key
            if (
                provider == "mli"
                and "mli" in self.data(-1)
                and self.explanation_type == "global"
            ):
                explanation_list = self.data(-1)["mli"]
                explanation_index = get_explanation_index(
                    explanation_list, "global_feature_importance"
                )
                scores = explanation_list[explanation_index]["value"]["scores"]
                sort_indexes = get_sort_indexes(
                    scores, sort_fn=lambda x: -abs(x), top_n=15
                )
                sorted_scores = mli_sort_take(
                    scores, sort_indexes, reverse_results=True
                )
                sorted_names = mli_sort_take(
                    self.feature_names, sort_indexes, reverse_results=True
                )
                return mli_plot_horizontal_bar(
                    sorted_scores,
                    sorted_names,
                    title="Overall Importance:<br>Coefficients",
                )
            # pragma: no cover
            msg = f"Visual provider {provider} not supported"
            raise RuntimeError(msg)
        data_dict = self.data(key)
        if data_dict is None:
            return None

        if self.explanation_type == "global" and key is None:
            data_dict = sort_take(
                data_dict, sort_fn=lambda x: -abs(x), top_n=15, reverse_results=True
            )
            return plot_horizontal_bar(
                data_dict, title="Overall Importance:<br>Coefficients"
            )

        return super().visualize(key)

class NAMClassifier(NAMBase):
    def __init__(
        self,
        units_multiplier: int = 2,
        num_basis_functions: int = 64,
        hidden_sizes: list = [64, 32],
        dropout: float = 0.1,
        feature_dropout: float = 0.05, 
        batch_size: int = 1024,
        num_workers: int = 0,
        num_epochs: int = 1000,
        log_dir: str = None,
        val_split: float = 0.15,
        device: str = 'cpu',
        lr: float = 0.02082,
        decay_rate: float = 0.0,
        output_reg: float = 0.2078,
        l2_reg: float = 0.0,
        save_model_frequency: int = 10,
        patience: int = 60,
        monitor_loss: bool = True,
        early_stop_mode: str = 'min',
        loss_func: Callable = None,
        metric: str = None,
        num_learners: int = 1,
        n_jobs: int = None,
        warm_start: bool = False,
        random_state: int = 42
    ) -> None:
        super(NAMClassifier, self).__init__(
            units_multiplier=units_multiplier,
            num_basis_functions=num_basis_functions,
            hidden_sizes=hidden_sizes,
            dropout=dropout,
            feature_dropout=feature_dropout,
            batch_size=batch_size,
            num_workers=num_workers,
            num_epochs=num_epochs,
            log_dir=log_dir,
            val_split=val_split,
            device=device,
            lr=lr,
            decay_rate=decay_rate,
            output_reg=output_reg,
            l2_reg=l2_reg,
            save_model_frequency=save_model_frequency,
            patience=patience,
            monitor_loss=monitor_loss,
            early_stop_mode=early_stop_mode,
            loss_func=loss_func,
            metric=metric,
            num_learners=num_learners,
            n_jobs=n_jobs,
            warm_start = warm_start,
            random_state=random_state
        )
        self.regression = False
        self._estimator_type = 'classifier'

    def fit(self, X, y, w=None):            
        if len(np.unique(y[~np.isnan(y)])) > 2:
            raise ValueError('More than two unique y-values detected. Multiclass classification not currently supported.')
        return super().fit(X, y, w)

    def predict_proba(self, X) -> ArrayLike:
        out = scipy.special.expit(super().predict(X))
        return out

    def predict(self, X) -> ArrayLike:
        return self.predict_proba(X).round()
    
class NAMRegressor(NAMBase):
    def __init__(
        self,
        units_multiplier: int = 2,
        num_basis_functions: int = 64,
        hidden_sizes: list = [64, 32],
        dropout: float = 0.1,
        feature_dropout: float = 0.05, 
        batch_size: int = 1024,
        num_workers: int = 0,
        num_epochs: int = 1000,
        log_dir: str = None,
        val_split: float = 0.15,
        device: str = 'cpu',
        lr: float = 0.02082,
        decay_rate: float = 0.0,
        output_reg: float = 0.2078,
        l2_reg: float = 0.0,
        save_model_frequency: int = 10,
        patience: int = 60,
        monitor_loss: bool = True,
        early_stop_mode: str = 'min',
        loss_func: Callable = None,
        metric: str = None,
        num_learners: int = 1,
        n_jobs: int = None,
        warm_start: bool = False,
        random_state: int = 42
    ) -> None:
        super(NAMRegressor, self).__init__(
            units_multiplier=units_multiplier,
            num_basis_functions=num_basis_functions,
            hidden_sizes=hidden_sizes,
            dropout=dropout,
            feature_dropout=feature_dropout,
            batch_size=batch_size,
            num_workers=num_workers,
            num_epochs=num_epochs,
            log_dir=log_dir,
            val_split=val_split,
            device=device,
            lr=lr,
            decay_rate=decay_rate,
            output_reg=output_reg,
            l2_reg=l2_reg,
            save_model_frequency=save_model_frequency,
            patience=patience,
            monitor_loss=monitor_loss,
            early_stop_mode=early_stop_mode,
            loss_func=loss_func,
            metric=metric,
            num_learners=num_learners,
            n_jobs=n_jobs,
            warm_start = warm_start,
            random_state=random_state
        )
        self.regression = True


class MultiTaskNAMClassifier(NAMClassifier):
    def __init__(
        self,
        units_multiplier: int = 2,
        num_basis_functions: int = 64,
        hidden_sizes: list = [64, 32],
        num_subnets: int = 2,
        dropout: float = 0.1,
        feature_dropout: float = 0.05, 
        batch_size: int = 1024,
        num_workers: int = 0,
        num_epochs: int = 1000,
        log_dir: str = None,
        val_split: float = 0.15,
        device: str = 'cpu',
        lr: float = 0.02082,
        decay_rate: float = 0.0,
        output_reg: float = 0.2078,
        l2_reg: float = 0.0,
        save_model_frequency: int = 10,
        patience: int = 60,
        monitor_loss: bool = True,
        early_stop_mode: str = 'min',
        loss_func: Callable = None,
        metric: str = None,
        num_learners: int = 1,
        n_jobs: int = None,
        warm_start: bool = False,
        random_state: int = 42
    ) -> None:
        super(MultiTaskNAMClassifier, self).__init__(
            units_multiplier=units_multiplier,
            num_basis_functions=num_basis_functions,
            hidden_sizes=hidden_sizes,
            dropout=dropout,
            feature_dropout=feature_dropout,
            batch_size=batch_size,
            num_workers=num_workers,
            num_epochs=num_epochs,
            log_dir=log_dir,
            val_split=val_split,
            device=device,
            lr=lr,
            decay_rate=decay_rate,
            output_reg=output_reg,
            l2_reg=l2_reg,
            save_model_frequency=save_model_frequency,
            patience=patience,
            monitor_loss=monitor_loss,
            early_stop_mode=early_stop_mode,
            loss_func=loss_func,
            metric=metric,
            num_learners=num_learners,
            n_jobs=n_jobs,
            warm_start = warm_start,
            random_state=random_state
        )
        self.num_subnets = num_subnets

    def _initialize_models(self, X, y):
        self.num_inputs = X.shape[1]
        self.num_tasks = y.shape[1] if len(y.shape) > 1 else 1
        self.models = []
        for _ in range(self.num_learners):
            model = MultiTaskNAM(num_inputs=X.shape[1],
                num_units=get_num_units(self.units_multiplier, self.num_basis_functions, X),
                num_subnets=self.num_subnets,
                num_tasks=y.shape[1],
                dropout=self.dropout,
                feature_dropout=self.feature_dropout,
                hidden_sizes=self.hidden_sizes)
            model.to(self.device)
            self.models.append(model)


class MultiTaskNAMRegressor(NAMRegressor):
    def __init__(
        self,
        units_multiplier: int = 2,
        num_basis_functions: int = 64,
        hidden_sizes: list = [64, 32],
        num_subnets: int = 2,
        dropout: float = 0.1,
        feature_dropout: float = 0.05, 
        batch_size: int = 1024,
        num_workers: int = 0,
        num_epochs: int = 1000,
        log_dir: str = None,
        val_split: float = 0.15,
        device: str = 'cpu',
        lr: float = 0.02082,
        decay_rate: float = 0.995,
        output_reg: float = 0.2078,
        l2_reg: float = 0.0,
        save_model_frequency: int = 10,
        patience: int = 60,
        monitor_loss: bool = True,
        early_stop_mode: str = 'min',
        loss_func: Callable = None,
        metric: str = None,
        num_learners: int = 1,
        n_jobs: int = None,
        warm_start: bool = False,
        random_state: int = 42
    ) -> None:
        super(MultiTaskNAMRegressor, self).__init__(
            units_multiplier=units_multiplier,
            num_basis_functions=num_basis_functions,
            hidden_sizes=hidden_sizes,
            dropout=dropout,
            feature_dropout=feature_dropout,
            batch_size=batch_size,
            num_workers=num_workers,
            num_epochs=num_epochs,
            log_dir=log_dir,
            val_split=val_split,
            device=device,
            lr=lr,
            decay_rate=decay_rate,
            output_reg=output_reg,
            l2_reg=l2_reg,
            save_model_frequency=save_model_frequency,
            patience=patience,
            monitor_loss=monitor_loss,
            early_stop_mode=early_stop_mode,
            loss_func=loss_func,
            metric=metric,
            num_learners=num_learners,
            n_jobs=n_jobs,
            warm_start = warm_start,
            random_state=random_state
        )
        self.num_subnets = num_subnets

    def _initialize_models(self, X, y):
        self.num_inputs = X.shape[1]
        self.num_tasks = y.shape[1] if len(y.shape) > 1 else 1
        self.models = []
        for _ in range(self.num_learners):
            model = MultiTaskNAM(num_inputs=X.shape[1],
                num_units=get_num_units(self.units_multiplier, self.num_basis_functions, X),
                num_subnets=self.num_subnets,
                num_tasks=y.shape[1],
                dropout=self.dropout,
                feature_dropout=self.feature_dropout,
                hidden_sizes=self.hidden_sizes)
            model.to(self.device)
            self.models.append(model)

def _hist_per_column(arr, feature_types=None):
    counts = []
    bin_edges = []

    if feature_types is not None:
        for i, feat_type in enumerate(feature_types):
            if feat_type == "continuous":
                count, bin_edge = np.histogram(arr[:, i], bins="doane")
                counts.append(count)
                bin_edges.append(bin_edge)
            elif feat_type in ("nominal", "ordinal"):
                # Todo: check if this call
                bin_edge, count = np.unique(arr[:, i], return_counts=True)
                counts.append(count)
                bin_edges.append(bin_edge)
    else:
        for i in range(arr.shape[1]):
            count, bin_edge = np.histogram(arr[:, i], bins="doane")
            counts.append(count)
            bin_edges.append(bin_edge)
    return counts, bin_edges