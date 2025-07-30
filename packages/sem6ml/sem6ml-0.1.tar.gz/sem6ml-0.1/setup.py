from setuptools import setup, find_packages

setup(
    name="sem6ml",
    version="0.1",
    packages=find_packages(),
    description="ML Lab Exercises Package",
    author="Machine Learning",
    install_requires=[
        "scikit-learn"
    ],
    python_requires='>=3.6',
)
