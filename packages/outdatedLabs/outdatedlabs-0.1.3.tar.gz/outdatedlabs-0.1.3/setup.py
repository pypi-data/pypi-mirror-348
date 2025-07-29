from setuptools import setup, find_packages

setup(
    name="outdatedLabs",
    version="0.1.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.31.0",
        "joblib>=1.3.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.0.0",
        "tqdm>=4.65.0",
    ],
    python_requires=">=3.8",
    author="OutDated Team",
    author_email="your.email@example.com",
    description="A secure package for training machine learning models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mouli51ch/OutDated",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 