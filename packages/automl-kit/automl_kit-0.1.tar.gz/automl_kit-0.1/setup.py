from setuptools import setup, find_packages

setup(
    name='automl-kit',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy', 'pandas', 'scikit-learn', 'matplotlib', 'seaborn'
    ],
    description='AutoML library that selects the best model automatically.',
    author='Tanmai Raghava',
    license='MIT'
)