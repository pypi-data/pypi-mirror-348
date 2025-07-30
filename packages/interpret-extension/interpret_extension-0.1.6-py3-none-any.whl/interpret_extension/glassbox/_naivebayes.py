from abc import abstractmethod

import numpy as np
from sklearn.base import ClassifierMixin, is_classifier
from sklearn.naive_bayes import GaussianNB as SKGaussianNB
from sklearn.naive_bayes import CategoricalNB as SKCategoricalNB
from sklearn.utils.validation import check_is_fitted

from ..api.base import ExplainerMixin
from ..api.templates import FeatureValueExplanation
from ..utils._clean_simple import clean_dimensions, typify_classification
from ..utils._clean_x import preclean_X
from ..utils._explanation import (
    gen_global_selector,
    gen_local_selector,
    gen_name_from_class,
    gen_perf_dicts,
)
from ..utils._unify_data import unify_data

class BaseNaiveBayes:
    """Base class for Naive Bayes interpretable model."""

    def __init__(
            self, feature_names=None, feature_types=None, nb_class=SKGaussianNB, **kwargs
    ):
        """Initializes class.
        
        Args:
            feature_names: List of feature names.
            feature_types: List of feature types.
            nb_class: A scikit-learn Gaussian Naive Bayes class.
            **kwargs: Kwargs pass to Naive Bayes class at initialization time.
        """
        self.feature_names = feature_names
        self.feature_types = feature_types
        self.nb_class = nb_class
        self.kwargs = kwargs

    @abstractmethod
    def _model(self):
        # This method should be overridden.
        return None

    def fit(self, X, y):
        """Fits the model.
        
        Args:
            X: Numpy array for training instances.
            y: Numpy array as training labels.
        """
        
        pass

    def predict(self, X):
        """Predicts on provided instances.
        
        Args:
            X: Numpy array for instances.
            
        Returns:
            Predicted class label per instance
        """
        
        check_is_fitted(self, "has_fitted_")

        X, n_samples = preclean_X(X, self.feature_names_in_, self.feature_types_in_)
        X, _, _ = unify_data(
            X, n_samples, self.feature_names_in_, self.feature_types_in_, False, 0
        )

        return self._model().predict(X)

    def predict_proba(self, X):
        """Probability estimates on provided instances.

        Args:
            X: Numpy array for instances.

        Returns:
            Probability estimate of instance for each class.
        """

        check_is_fitted(self, "has_fitted_")

        X, n_samples = preclean_X(X, self.feature_names_in_, self.feature_types_in_)
        X, _, _ = unify_data(
            X, n_samples, self.feature_names_in_, self.feature_types_in_, False, 0
        )

        return self.model.predict_proba(X)

    def explain_local(self, X, y=None, name=None):
        """Provides local explanations for provided instances.

        Args:
            X: Numpy array for X to explain.
            y: Numpy vector for y to explain.
            name: User-defined explanation name.

        Returns:
            An explanation object, visualizing feature-value pairs
            for each instance as horizontal bar charts.
        """

        pass
    
    def explain_global(self, name=None):
        """Provides global explanations.

        Args:
            name: User-defined explanation name.

        Returns:
            An explanation object, visualizing feature-value pairs
            as horizontal bar charts.
        """

        pass

class GaussianNB(BaseNaiveBayes, ClassifierMixin, ExplainerMixin):
    """
    Base class for Naive Bayes interpretable model.
    """

    available_explanations = ["local", "global"]
    explainer_type = "model"

    def __init__(
            self, feature_names=None, feature_types=None, nb_class=SKGaussianNB, **kwargs
    ):
        """
        Initializes class.

        Args:
            feature_names: List of feature names.
            feature_types: List of feature types.
            nb_class: A scikit-learn Gaussian Naive Bayes class.
            **kwargs: Kwargs pass to Naive Bayes class at initialization time.
        """
        super().__init__(feature_names, feature_types, nb_class, **kwargs)

    def _model(self):
        return self.model

    def fit(self, X, y):
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
        
        if is_classifier(self.nb_class):
            y = typify_classification(y)
        else:
            y = y.astype(np.float64, copy=False)

        X, n_samples = preclean_X(X, self.feature_names, self.feature_types, len(y))

        X, self.feature_names_in_, self.feature_types_in_ = unify_data(
            X, n_samples, self.feature_names, self.feature_types, False, 0
        )

        X = X.astype(np.float64)

        self.model = self.nb_class(**self.kwargs)
        self.model.fit(X, y)

        self.n_features_in_ = len(self.feature_names_in_)
        if is_classifier(self.nb_class):
            self.classes_ = self.model.classes_

        self.X_mins_ = np.min(X, axis=0)
        self.X_maxs_ = np.max(X, axis=0)

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

        self.classes_ = self.model.classes_

        self.has_fitted_ = True

        return self
    
    def explain_local(self, X, y=None, name=None):
        """Provides local explanations for provided instances.

        Args:
            X: Numpy array for X to explain.
            y: Numpy vector for y to explain.
            name: User-defined explanation name.

        Returns:
            An explanation object, visualizing feature-value pairs
            for each instance as horizontal bar charts.
        """

        check_is_fitted(self, "has_fitted_")

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

        model = self._model()

        classes = np.array([0, 1], np.int64)
        is_classification = is_classifier(self)

        # Here starts our modifications (for binary classification)
        def conditional_probabilities(model, X):
            X = X.astype(float)

            class_0_cp = np.exp(-0.5 * ((X - model.theta_[0, :]) ** 2) / (model.var_[0, :])) / (np.sqrt(2 * np.pi * model.var_[0, :]))
            class_1_cp = np.exp(-0.5 * ((X - model.theta_[1, :]) ** 2) / (model.var_[1, :])) / (np.sqrt(2 * np.pi * model.var_[1, :]))
            
            return class_0_cp, class_1_cp

        class_0_prior = model.class_prior_[0]
        class_1_prior = model.class_prior_[1]
        predictions = self.predict_proba(X)
        intercept = np.log(class_0_prior / class_1_prior)

        data_dicts = []
        scores_list = []
        perf_list = []
        perf_dicts = gen_perf_dicts(predictions, y, is_classification, classes)
        for i, instance in enumerate(X):
            c0_cp, c1_cp = conditional_probabilities(model, instance)
            scores = np.log(c1_cp / c0_cp)
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
        """Provides global explanations.

        Args:
            name: User-defined explanation name.

        Returns:
            An explanation object, visualizing feature-value pairs
            as horizontal bar charts.
        """

        check_is_fitted(self, "has_fitted_")

        if name is None:
            name = gen_name_from_class(self)

        model = self._model()

        # TO DELETE
        def get_ratio(model, value, index):
            class_0_cp = np.exp(-0.5 * ((value - model.theta_[0, index]) ** 2) / (model.var_[0, index])) / (np.sqrt(2 * np.pi * model.var_[0, index]))
            class_1_cp = np.exp(-0.5 * ((value - model.theta_[1, index]) ** 2) / (model.var_[1, index])) / (np.sqrt(2 * np.pi * model.var_[1, index]))
            return np.log(class_1_cp / class_0_cp)

        def get_ratio_modified(model, value, index):
            numerator_term_0 = ((value - model.theta_[0, index]) ** 2) / (model.var_[0, index])
            denominator_term_0 = np.sqrt(model.var_[0, index])

            numerator_term_1 = ((value - model.theta_[1, index]) ** 2) / (model.var_[1, index])
            denominator_term_1 = np.sqrt(model.var_[1, index])

            log_ratio = -0.5 * (numerator_term_1 - numerator_term_0) + np.log(denominator_term_0 / denominator_term_1)
            return log_ratio
    
        keep_idxs = []
        specific_data_dicts = []
        for index, _ in enumerate(self.feature_names_in_):
            keep_idxs.append(index)

            min_feature_val = self.X_mins_[index]
            max_feature_val = self.X_maxs_[index]
            
            grid_points = np.linspace(min_feature_val, max_feature_val, 5000)
            model_graph = [get_ratio_modified(model, val, index) for val in grid_points]

            y_scores = model_graph

            data_dict = {
                "names": grid_points,
                "scores": y_scores,
                "density": {
                    "scores": self.bin_counts_[index],
                    "names": self.bin_edges_[index],
                }
            }

            specific_data_dicts.append(data_dict)

        overall_data_dict = None

        internal_obj = {
            "overall": overall_data_dict,
            "specific": specific_data_dicts,
            "mli": [
                {
                    "explanation_type": "global_gaussian_naive_bayes"
                }
            ]
        }

        return NaiveBayesExplanation(
            "global",
            internal_obj,
            feature_names=self.feature_names_in_,
            feature_types=self.feature_types_in_,
            name=name,
            selector=self.global_selector_,
        )
    
class CategoricalNB(BaseNaiveBayes, ClassifierMixin, ExplainerMixin):
    """
    Base class for Naive Bayes interpretable model.
    """

    available_explanations = ["local", "global"]
    explainer_type = "model"

    def __init__(
            self, feature_names=None, feature_types=None, nb_class=SKCategoricalNB, **kwargs
    ):
        """
        Initializes class.

        Args:
            feature_names: List of feature names.
            feature_types: List of feature types.
            nb_class: A scikit-learn Gaussian Naive Bayes class.
            **kwargs: Kwargs pass to Naive Bayes class at initialization time.
        """
        super().__init__(feature_names, feature_types, nb_class, **kwargs)

    def _model(self):
        return self.model

    def fit(self, X, y):
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
        
        if is_classifier(self.nb_class):
            y = typify_classification(y)
        else:
            y = y.astype(np.float64, copy=False)

        X, n_samples = preclean_X(X, self.feature_names, self.feature_types, len(y))

        X, self.feature_names_in_, _ = unify_data(
            X, n_samples, self.feature_names, self.feature_types, False, 0
        )

        self.feature_types_in_ = ["nominal"] * len(self.feature_names_in_)

        self.model = self.nb_class(**self.kwargs)
        self.model.fit(X, y)

        self.n_features_in_ = len(self.feature_names_in_)
        if is_classifier(self.nb_class):
            self.classes_ = self.model.classes_

        self.X_mins_ = np.min(X, axis=0)
        self.X_maxs_ = np.max(X, axis=0)
        self.categorical_uniq_ = {}

        for i, feature_type in enumerate(self.feature_types_in_):
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

        self.classes_ = self.model.classes_

        self.has_fitted_ = True

        return self
    
    def explain_local(self, X, y=None, name=None):
        """Provides local explanations for provided instances.

        Args:
            X: Numpy array for X to explain.
            y: Numpy vector for y to explain.
            name: User-defined explanation name.

        Returns:
            An explanation object, visualizing feature-value pairs
            for each instance as horizontal bar charts.
        """

        check_is_fitted(self, "has_fitted_")

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

        model = self._model()

        classes = np.array([0, 1], np.int64)
        is_classification = is_classifier(model)

        def conditional_probabilities(model, X):
            cp_0 = np.zeros(X.shape[0])
            cp_1 = np.zeros(X.shape[0])
            for j in range(X.shape[0]):
                cp_0[j] = np.exp(model.feature_log_prob_[j][0][int(X[j])])
                cp_1[j] = np.exp(model.feature_log_prob_[j][1][int(X[j])])
            return cp_0, cp_1

        class_0_prior = model.class_count_[0] / model.class_count_.sum()
        class_1_prior = model.class_count_[1] / model.class_count_.sum()
        predictions = self.predict_proba(X)
        intercept = np.log(class_1_prior / class_0_prior)

        data_dicts = []
        scores_list = []
        perf_list = []
        perf_dicts = gen_perf_dicts(predictions, y, is_classification, classes)
        for i, instance in enumerate(X):
            c0_cp, c1_cp = conditional_probabilities(model, instance)
            scores = np.log(c1_cp / c0_cp)
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
        """Provides global explanation for model.

        Args:
            name: User-defined explanation name.

        Returns:
            An explanation object,
            visualizing feature-value pairs as horizontal bar chart.
        """

        check_is_fitted(self, "has_fitted_")

        if name is None:
            name = gen_name_from_class(self)

        model = self._model()

        def get_ratio(model, value, index):
            cp_0 = np.exp(model.feature_log_prob_[index][0][int(value)])
            cp_1 = np.exp(model.feature_log_prob_[index][1][int(value)])
            return np.log(cp_0 / cp_1)

        # Add per feature graph
        data_dicts = []
        feature_list = []
        density_list = []
        keep_idxs = []
        importances = []
        for index, _ in enumerate(self.feature_names_in_):
            keep_idxs.append(index)
            bin_labels = self.categorical_uniq_[index]
            histogram_weights = model.category_count_[index]
            
            names = bin_labels
            densities = list(np.array(histogram_weights).sum(axis=0))

            model_graph = [get_ratio(model, x, index) for x in bin_labels]

            scores = list(model_graph)

            importance = sum([(d / sum(densities))*abs(s)
                              for d,s in zip(densities, scores)
                              if d > 0])
            importances.append(importance)

            density_dict = {
                "names": names,
                "scores": densities,
            }

            feature_dict = {
                "type": "univariate",
                "names": bin_labels,
                "scores": scores,
                "scores_range": None,
                "upper_bounds": None,
                "lower_bounds": None,
            }

            feature_list.append(feature_dict)
            density_list.append(density_dict)

            data_dict = {
                "type": "univariate",
                "names": bin_labels,
                "scores": scores,
                "scores_range": None,
                "upper_bounds": None,
                "lower_bounds": None,
                "density": {
                    "names": names,
                    "scores": densities,
                },
            }

            if hasattr(self, "classes_"):
                # Classes should be NumPy array, convert to list.
                data_dict["meta"] = {"label_names": self.classes_.tolist()}

            data_dicts.append(data_dict)
        

        term_names = self.feature_names_in_
        term_types = self.feature_types_in_

        overall_dict = {
            "type": "univariate",
            "names": [term_names[i] for i in keep_idxs],
            "scores": importances,
        }

        internal_obj = {
            "overall": overall_dict,
            "specific": data_dicts,
            "mli": [
                {
                    "explanation_type": "global_categorical_naive_bayes",
                    "value": {"feature_list": feature_list},
                },
                {"explanation_type": "density", "value": {"density": density_list}},
            ],
        }

        return NaiveBayesExplanation(
            "global",
            internal_obj,
            feature_names=[term_names[i] for i in keep_idxs],
            feature_types=[term_types[i] for i in keep_idxs],
            name=name,
            selector=gen_global_selector(
                self.n_features_in_,
                [term_names[i] for i in keep_idxs],
                [term_types[i] for i in keep_idxs],
                [len(x) for x in self.categorical_uniq_.values()],
                None,
            ),
        )

class NaiveBayesExplanation(FeatureValueExplanation):
    """Visualizes specifically for NB methods."""

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
        from ..visual.plot import (
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
                data_dict, title="Overall Importance:<br>Coefficients", start_zero=True
            )

        return super().visualize(key)    

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