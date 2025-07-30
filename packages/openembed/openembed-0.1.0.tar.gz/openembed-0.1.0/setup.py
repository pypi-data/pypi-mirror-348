"""Setup configuration for the openembed package."""

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="openembed",
        version="0.1.0",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        install_requires=[
            "numpy",
            "requests",
        ],
        extras_require={
            "openai": ["openai>=1.0.0"],
            "cohere": ["cohere"],
            "huggingface": ["transformers", "torch"],
            "voyageai": ["voyageai"],
            "amazon": ["boto3"],
            "all": [
                "openai>=1.0.0",
                "cohere",
                "transformers",
                "torch",
                "voyageai",
                "boto3",
            ],
            "dev": [
                "pytest",
                "pytest-cov",
                "black",
                "isort",
                "flake8",
                "mypy",
            ],
        },
        python_requires=">=3.8",
    )