from setuptools import setup, find_packages

setup(
    name='tl_lab',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'tensorflow',
        'matplotlib',
        'kagglehub',
        'opendatasets',
        'scikit-learn',
        'transformers',
        'datasets',
        'torch',
        'seaborn',
        # Add other dependencies you use
    ],
    author='Your Name',
    description='Collection of ML experiments as reusable package',
)
