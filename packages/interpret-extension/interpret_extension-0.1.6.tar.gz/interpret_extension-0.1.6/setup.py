from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name="interpret-extension",
    version="0.1.6",
    description="This extension aims to expand InterpretML by \
                 integrating probabilistic models while leveraging the existing \
                 explanation mechanisms provided by the library. By doing so, we \
                 enable users to analyze uncertainty, quantify probabilistic \
                 predictions, and gain deeper insights into model behavior beyond point estimates.",
    author="Javier Pérez Vargas",
    author_email="javipv2003pv@gmail.com",
    url="https://github.com/bmihaljevic/tfg-interpretml",
    packages=find_packages(),
    long_description=readme,
    long_description_content_type='text/markdown',
    install_requires=[
        "joblib==1.4.2",
        "numpy==1.26.4",
        "pandas==2.2.3",
        "pyAgrum==1.15.1",
        "scikit_learn==1.3.2",
        "scipy==1.13.1",
        "torch==2.6.0",
        "tqdm==4.66.2",
        "loguru==0.7.3",
        "tensorboard==2.19.0",
        "matplotlib-inline==0.1.7",
        "ipython==8.18.1",
        "requests==2.32.3",
        "Flask==2.2.2",
        "Werkzeug==2.2.2",
        "gevent==24.11.1",
        "dash==2.18.2",
        "dash-cytoscape==1.0.2",
        "gevent==24.11.1",
    ],
    extras_require={
        "debug": ["psutil==6.1.1"],
        "notebook": ["ipykernel==6.29.5", "ipython==8.18.1"],
        # Plotly (required if .visualize is ever called)
        "plotly": ["plotly==5.24.1"],
        # Explainers
        "lime": ["lime==0.2.0.1"],
        "sensitivity": ["SALib==1.5.1"],
        "shap": ["shap==0.46.0", "dill>=0.2.5"],
        "linear": [],
        "skoperules": ["skope-rules>=1.0.1"],
        "treeinterpreter": ["treeinterpreter==0.2.3"],
        "aplr": ["aplr==10.8.0"],
        # Testing
        "testing": [
            "scikit-learn>=1.0.0",
            "pytest>=4.3.0",
            "pytest-runner>=4.4",
            "pytest-xdist>=1.29",
            "nbconvert>=5.4.1",
            "selenium>=3.141.0",
            "pytest-cov>=2.6.1",
            "ruff>=0.1.2",
            "jupyter>=1.0.0",
            "ipywidgets==8.1.5",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)