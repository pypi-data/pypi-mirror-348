from setuptools import setup, find_packages

setup(
    name="kanmanipriya_ml_lab",
    version="0.1",
    packages=find_packages(),
    description="ML Lab Exercises Package",
    author="pradhanya",
    install_requires=[
        "scikit-learn"
    ],
    python_requires='>=3.6',
)
