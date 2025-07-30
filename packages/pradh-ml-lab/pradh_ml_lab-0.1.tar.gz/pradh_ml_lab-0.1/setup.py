from setuptools import setup, find_packages

setup(
    name="pradh_ml_lab",
    version="0.1",
    packages=find_packages(),
    description="ML Lab Exercises Package",
    author="Pradhanya",
    install_requires=[
        "scikit-learn"
    ],
    python_requires='>=3.6',
)
