# Extending [InterpretML](https://github.com/interpretml/interpret)

As it Github page says:

"**InterpretML** is an open-source package that incorporates state-of-the-art machine learning **interpretability techniques** under one roof. With this package, you can train interpretable glassbox models and explain blackbox systems. InterpretML helps you understand your model's global behavior, or understand the reasons behind individual predictions."

## Installation

The easiest way to install this extension of **InterpretML** is by following these steps:

1. Create a new conda environment:
```
conda create --name {env_name} python=3.9
```

2. Activate the environment:
```
conda activate {env_name}
```

3. Navigate to the root directory and install:
```
pip install ./interpret/python/interpret-core
```

While you can choose not to use conda, it is recommended to avoid potential conflicts with dependencies.

## Objective of this Extension

Currently, InterpretML implements several interpretable models, such as Explainable Boosting Machines (EBMs), decision trees, and linear models, along with various explanation techniques for blackbox models.

This extension aims to expand InterpretML by integrating probabilistic models while leveraging the existing explanation mechanisms provided by the library. By doing so, we enable users to analyze uncertainty, quantify probabilistic predictions, and gain deeper insights into model behavior beyond point estimates.

## How InterpretML visualize glassbox models?

InterpretML uses two main ways to explain these type of models:

- **Global Explanations**: These explanations provide insights into how a model makes predictions across the **entire dataset**.

<p align="center">
  <img width="700" align="center" alt="Image" src="https://raw.githubusercontent.com/javipzv/raw-images/refs/heads/main/images/global_explanation.png" />
</p>

<br>

- **Local Explanations**: These explanations focus on **individual predictions**, showing why the model made a specific decision for a given instance.

<p align="center">
  <img width="700" align="center" alt="Image" src="https://github.com/javipzv/raw-images/blob/main/images/local_explanation.png?raw=true" />
</p>
<br>

The main goal will be to use both global and local visualizations for different models that InterpretML does not currently implement.

## Adding new models

The new models incorporated in this extension are:

- **Naive Bayes** (Gaussian and Categorical): A simple yet powerful probabilistic model based on Bayes' theorem. It assumes feature independence, making it highly efficient for classification tasks.

- **Linear Discriminant Model**: A classification model that finds the linear combination of features that best separates two or more classes. It is particularly useful for dimensionality reduction while preserving class separability.

- **TAN** (Tree Augmented Naive Bayes): An extension of Naive Bayes that allows for dependencies between features using a tree structure, improving its expressiveness while maintaining efficiency.

- **Bayesian Network**: A probabilistic graphical model that represents variables and their conditional dependencies via a directed acyclic graph (DAG). It is useful for modeling complex probabilistic relationships.

- **NAM** (Neural Additive Model): A neural network-based approach that extends Generalized Additive Models (GAMs) by learning feature contributions in a flexible and interpretable manner.

These models will be integrated with InterpretML's existing explanation mechanisms, ensuring users can interpret their predictions using global and local explanations.
