"""List all extra dependencies to be installed for Konfuzio SDK's AIs and dev mode."""

# Keep track with AI type needs which package in order to make bento builds as small as possible.
CATEGORIZATION_EXTRAS = [
    'torch>=1.8.1',
    'torchvision>=0.9.1',
    'transformers==4.30.2',
    'timm==0.6.7',
]

FILE_SPLITTING_EXTRAS = [
    'accelerate==0.20.1',
    'datasets==2.14.6',
    'mlflow==2.17.0',
    'tensorflow-cpu==2.12.0',
    'torch>=1.8.1,<2.6.0',
    'transformers==4.30.2',
]

EXTRAS = {
    'dev': [
        'autodoc_pydantic==2.2.0',
        'coverage==7.3.2',
        'jupytext==1.16.4',
        'pytest>=7.1.2',
        'pre-commit>=2.20.0',
        'parameterized>=0.8.1',
        'Sphinx==5.0.0',
        'sphinx-toolbox==3.4.0',
        'sphinx-reload==0.2.0',
        'sphinx-notfound-page==0.8',
        'm2r2==0.3.2',
        'nbval==0.10.0',
        'sphinx-sitemap==2.2.0',
        'sphinx-rtd-theme==1.0.0',
        'sphinxcontrib-jquery',
        'sphinxcontrib-mermaid==0.8.1',
        'sphinx-copybutton==0.5.2',
        'myst_nb==0.17.2',
        'ruff',
        'pytest-rerunfailures',
    ],
    'ai': list(
        set(
            [
                'chardet==5.1.0',
                'evaluate==0.4.3',
                'spacy>=2.3.5,<3.8.0',
            ]
            + CATEGORIZATION_EXTRAS
            + FILE_SPLITTING_EXTRAS
        )
    ),
}
