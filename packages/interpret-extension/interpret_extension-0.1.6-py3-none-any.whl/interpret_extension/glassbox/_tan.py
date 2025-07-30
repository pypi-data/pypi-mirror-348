# Copyright (c) 2023 The InterpretML Contributors
# Distributed under the MIT software license

from abc import abstractmethod

import numpy as np
from sklearn.base import ClassifierMixin, is_classifier
from pyAgrum.skbn import BNClassifier
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


class BaseTAN:
    """Base Tree Augmented Naive Bayes.

    Currently wrapper around linear models in pyAgrum.

    https://github.com/agrumery/aGrUM

    """

    available_explanations = ["local", "global"]
    explainer_type = "model"

    def __init__(
        self, 
        feature_names=None, 
        feature_types=None, 
        TAN_class=BNClassifier(
            learningMethod="TAN", prior= 'Smoothing', priorWeight = 0.5,
            discretizationStrategy = 'quantile', usePR = True, significant_digit = 13
        ), **kwargs
    ):
        """Initializes class.

        Args:
            feature_names: List of feature names.
            feature_types: List of feature types.
            linear_class: A pyAgrum TAN class.
            **kwargs: Kwargs pass to TAN class at initialization time.
        """
        self.feature_names = feature_names
        self.feature_types = feature_types
        self.TAN_class = TAN_class
        self.kwargs = kwargs

    @abstractmethod
    def _model(self):
        # This method should be overridden.
        return None

    def fit(self, X, y):
        """Fits model to provided instances.

        Args:
            X: Numpy array for training instances.
            y: Numpy array as training labels.

        Returns:
            Itself.
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

        X, n_samples = preclean_X(X, self.feature_names, self.feature_types, len(y))
        
        model = self._model()
        model.fit(X, y)

        X, self.feature_names_in_, self.feature_types_in_ = unify_data(
            X, n_samples, self.feature_names, self.feature_types, False, 0
        )

        # NOTE: Fix for considering only categorical features
        self.feature_types_in_ = ["nominal"] * len(self.feature_names_in_)

        self.target = model.target

        self.parents = {}
        for i, feature in enumerate(self.feature_names_in_):
            self.parents[feature] = model.bn.parents(feature)

        self.nameFromId = {}
        for i, feature in enumerate(self.feature_names_in_):
            self.nameFromId[model.bn.idFromName(feature)] = feature

        self.n_features_in_ = len(self.feature_names_in_)
        if is_classifier(self):
            # self.classes_ = model.classes_
            self.classes = np.array([0, 1], dtype=np.int64)

        self.X_mins_ = np.min(X, axis=0)
        self.X_maxs_ = np.max(X, axis=0)

        self.categorical_uniq_ = {}
        for i, feature_type in enumerate(self.feature_types_in_):
            self.categorical_uniq_[i] = sorted(set(X[:, i]))

        self.densities = {}
        for i, feature in enumerate(self.feature_names_in_):
            n_diff_vals = len(self.categorical_uniq_[i])
            if n_diff_vals < 100:
                self.densities[i] = np.zeros(n_diff_vals)
                for j, val in enumerate(self.categorical_uniq_[i]):
                    self.densities[i][j] = np.sum(X[:, i] == val)
            else:
                raise ValueError("Only categorical features are supported.")

        unique_val_counts = np.zeros(len(self.feature_names_in_), dtype=np.int64)
        for col_idx in range(len(self.feature_names_in_)):
            X_col = X[:, col_idx]
            unique_val_counts[col_idx] = len(np.unique(X_col))

        self.priors_ = np.zeros(len(self.classes), dtype=np.float64)
        for i, class_ in enumerate(self.classes):
            self.priors_[i] = np.sum(y == class_)
        self.priors_ /= len(y)

        self.global_selector_ = gen_global_selector(
            len(self.feature_names_in_),
            self.feature_names_in_,
            self.feature_types_in_,
            unique_val_counts,
            None,
        )
        self.bin_counts_, self.bin_edges_ = _hist_per_column(X, self.feature_types_in_)

        self.has_fitted_ = True

        return self

    def predict(self, X):
        """Predicts on provided instances.

        Args:
            X: Numpy array for instances.

        Returns:
            Predicted class label per instance.
        """

        check_is_fitted(self, "has_fitted_")

        X, n_samples = preclean_X(X, self.feature_names_in_, self.feature_types_in_)
        X, _, _ = unify_data(
            X, n_samples, self.feature_names_in_, self.feature_types_in_, False, 0
        )

        return self._model().predict(X)

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
            # TODO: we could probably handle this case
            msg = "X has zero samples"
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
                feature = self.feature_names_in_[j]
                cpt = model.bn.cpt(feature)
                n_parents = len(self.parents[feature])
                value = X[j]

                if n_parents == 1:
                    cp_0[j] = cpt[0, value]
                    cp_1[j] = cpt[1, value]
                
                elif n_parents == 2:
                    direct_parent = model.bn.parents(feature) - {model.bn.idFromName(self.target)}
                    direct_parent_name = self.nameFromId[list(direct_parent)[0]]
                    idx_parent = self.feature_names_in_.index(direct_parent_name)
                    parent_value = X[idx_parent]
                    cp_0[j] = cpt[0, parent_value, value]
                    cp_1[j] = cpt[1, parent_value, value]

            return cp_0, cp_1

        intercept = np.log(self.priors_[1] / self.priors_[0])
        predictions = model.predict_proba(X)

        data_dicts = []
        scores_list = []
        perf_list = []
        perf_dicts = gen_perf_dicts(predictions, y, is_classification, classes)
        for i, instance in enumerate(X):
            cp_0, cp_1 = conditional_probabilities(model, instance)
            scores = np.log(cp_1 / cp_0)
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
                "value": {"dataset_x": X, "dataset_y": y},
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

        # TODO
        intercept = 0
        coef = []

        def calculate_model_graph(feat_cpt, n_parents):
            if n_parents == 1:
                ratios_class_0 = feat_cpt[0, :]
                ratios_class_1 = feat_cpt[1, :]
            elif n_parents == 2:
                ratios_class_0 = feat_cpt[0, :, :]
                ratios_class_1 = feat_cpt[1, :, :]
            else:
                raise ValueError("Only 1 or 2 parents are supported for TAN model.")
            
            # TODO: check if this is correct (maybe class_0 and class_1 should be swapped)
            return np.log(ratios_class_1 / ratios_class_0)
        
        # TODO
        overall_data_dict = {
            "names": self.feature_names_in_,
            "scores": list(coef),
            "extra": {"names": ["Intercept"], "scores": [intercept]},
        }

        specific_data_dicts = []
        feature_list = []
        term_names = []
        term_types = []
        keep_idxs = []
        for index, _feature in enumerate(self.feature_names_in_):
            keep_idxs.append(index)

            feat_parents = self.parents[_feature]
            feat_cpt = model.bn.cpt(_feature)
                        
            feat_min = self.X_mins_[index]
            feat_max = self.X_maxs_[index]
            feat_type = self.feature_types_in_[index]

            feat_density = self.densities[index]
            bounds = (feat_min, feat_max)

            n_parents = len(feat_parents)

            if n_parents == 1:
                term_names.append(_feature)
                term_types.append(feat_type)
                bin_labels = self.categorical_uniq_[index]

                names = bin_labels

                model_graph = calculate_model_graph(feat_cpt, n_parents)

                scores = list(model_graph)

                feature_dict = {
                    "type": "univariate",
                    "names": bin_labels,
                    "scores": scores,
                    "scores_range": None,
                    "upper_bounds": None,
                    "lower_bounds": None,
                }

                feature_list.append(feature_dict)

                data_dict = {
                    "type": "univariate",
                    "names": bin_labels,
                    "scores": scores,
                    "scores_range": None,
                    "upper_bounds": None,
                    "lower_bounds": None,
                    "density": {
                        "names": names,
                        "scores": feat_density,
                    },
                }

                if hasattr(self, "classes_"):
                    # Classes should be NumPy array, convert to list.
                    data_dict["meta"] = {"label_names": self.classes_.tolist()}
                
            elif n_parents == 2:
                # self.feature_types_in_[index] = "interaction"

                bin_labels_left = self.categorical_uniq_[index]

                direct_parent = model.bn.parents(_feature) - {model.bn.idFromName(self.target)}
                name_parent = self.nameFromId[list(direct_parent)[0]]

                term_names.append(f"{_feature} & {name_parent}")
                term_types.append("interaction")

                bin_labels_right = self.categorical_uniq_[list(direct_parent)[0]]

                model_graph = calculate_model_graph(feat_cpt, n_parents)

                feature_dict = {
                    "type": "interaction",
                    "left_names": bin_labels_left,
                    "right_names": bin_labels_right,
                    "scores": model_graph,
                    "scores_range": bounds,
                }
                feature_list.append(feature_dict)

                data_dict = {
                    "type": "interaction",
                    "left_names": bin_labels_left,
                    "right_names": bin_labels_right,
                    "scores": model_graph,
                    "scores_range": bounds,
                }

            specific_data_dicts.append(data_dict)

        internal_obj = {
            "overall": overall_data_dict,
            "specific": specific_data_dicts,
            "mli": [
                {
                    "explanation_type": "ebm_global",
                    "value": {"feature_list": feature_list},
                }
           ],
        }

        return TANExplanation(
            "global",
            internal_obj,
            feature_names=[term_names[i] for i in keep_idxs],
            feature_types=[term_types[i] for i in keep_idxs],
            name=name,
            selector=gen_global_selector(
                self.n_features_in_,
                [term_names[i] for i in keep_idxs],
                [term_types[i] for i in keep_idxs],
                None,
                None
            )
            ,
        )


class TANExplanation(FeatureValueExplanation):
    """Visualizes specifically for EBM."""

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
        """Initialize class.

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
            feature_names=feature_names,
            feature_types=feature_types,
            name=name,
            selector=selector,
        )

    def visualize(self, key=None):
        """Provide interactive visualizations.

        Args:
            key: Either a scalar or list
                that indexes the internal object for sub-plotting.
                If an overall visualization is requested, pass None.

        Returns:
            A Plotly figure.

        """
        from ..visual.plot import (
            is_multiclass_global_data_dict,
            plot_continuous_bar,
            plot_horizontal_bar,
            sort_take,
        )

        data_dict = self.data(key)
        if data_dict is None:
            return None

        # Overall global explanation
        if self.explanation_type == "global" and key is None:
            data_dict = sort_take(
                data_dict, sort_fn=lambda x: -abs(x), top_n=15, reverse_results=True
            )
            title = "Global Term/Feature Importances"

            figure = plot_horizontal_bar(
                data_dict,
                title=title,
                start_zero=True,
                xtitle="Mean Absolute Score (Weighted)",
            )

            figure._interpret_help_text = (
                "The term importances are the mean absolute "
                "contribution (score) each term (feature or interaction) makes to predictions "
                "averaged across the training dataset. Contributions are weighted by the number "
                "of samples in each bin, and by the sample weights (if any). The 15 most "
                "important terms are shown."
            )
            figure._interpret_help_link = "https://github.com/interpretml/interpret/blob/develop/docs/interpret/python/examples/group-importances.ipynb"

            return figure

        # Per term global explanation
        if self.explanation_type == "global":
            title = f"Term: {self.feature_names[key]} ({self.feature_types[key]})"

            if self.feature_types[key] == "continuous":
                xtitle = self.feature_names[key]

                if is_multiclass_global_data_dict(data_dict):
                    figure = plot_continuous_bar(
                        data_dict,
                        multiclass=True,
                        show_error=False,
                        title=title,
                        xtitle=xtitle,
                    )
                else:
                    figure = plot_continuous_bar(data_dict, title=title, xtitle=xtitle)

            elif (
                self.feature_types[key] == "nominal"
                or self.feature_types[key] == "ordinal"
                or self.feature_types[key] == "interaction"
            ):
                figure = super().visualize(key, title)
                figure._interpret_help_text = (
                    f"The contribution (score) of the term {self.feature_names[key]} to predictions "
                    "made by the model."
                )
            else:  # pragma: no cover
                msg = f"Not supported configuration: {self.explanation_type}, {self.feature_types[key]}"
                raise Exception(msg)

            figure._interpret_help_text = (
                "The contribution (score) of the term "
                f"{self.feature_names[key]} to predictions made by the model. For classification, "
                "scores are on a log scale (logits). For regression, scores are on the same "
                "scale as the outcome being predicted (e.g., dollars when predicting cost). "
                "Each graph is centered vertically such that average prediction on the train "
                "set is 0."
            )
            return figure

        # Local explanation graph
        if self.explanation_type == "local":
            figure = super().visualize(key)
            figure.update_layout(
                title="Local Explanation (" + figure.layout.title.text + ")",
                xaxis_title="Contribution to Prediction",
            )
            figure._interpret_help_text = (
                "A local explanation shows the breakdown of how much "
                "each term contributed to the prediction for a single sample. The intercept "
                "reflects the average case. In regression, the intercept is the average y-value "
                "of the train set (e.g., $5.51 if predicting cost). In classification, the "
                "intercept is the log of the base rate (e.g., -2.3 if the base rate is 10%). The "
                "15 most important terms are shown."
            )

            return figure
        msg = (
            f"`explainer_type has to be 'global' or 'local', got {self.explainer_type}."
        )
        raise NotImplementedError(msg)

class TANClassifier(BaseTAN, ClassifierMixin, ExplainerMixin):
    """Tree Augmented Naive Bayes.

    Currently wrapper around TAN model in pyAgrum: https://github.com/agrumery/aGrUM
    """

    def __init__(
        self, feature_names=None, feature_types=None, TAN_class=BNClassifier(
            learningMethod="TAN", prior= 'Smoothing', priorWeight = 0.5,
            discretizationStrategy = 'quantile', usePR = True, significant_digit = 13
        ), **kwargs
    ):
        """Initializes class.

        Args:
            feature_names: List of feature names.
            feature_types: List of feature types.
            TAN_class: A pyAgrum TAN class.
            **kwargs: Kwargs pass to linear class at initialization time.
        """
        super().__init__(feature_names, feature_types, TAN_class, **kwargs)

    def _model(self):
        return self.sk_model_

    def fit(self, X, y):
        """Fits model to provided instances.

        Args:
            X: Numpy array for training instances.
            y: Numpy array as training labels.

        Returns:
            Itself.
        """
        self.sk_model_ = self.TAN_class
        return super().fit(X, y)

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

        return self._model().predict_proba(X)


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
