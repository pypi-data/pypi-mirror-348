# setup.py - Package Setup
# =========================

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="contextwormhole",
    version="1.2.0",
    author="ContextWormhole Team",
    author_email="team@contextwormhole.dev",
    description="Teleport beyond context limits with transformers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/contextwormhole/contextwormhole",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "pytest-mock>=3.6.0",
            "pytest-benchmark>=3.4.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ],
        "lint": [
            "black>=22.0.0",
            "flake8>=4.0.0",
            "isort>=5.10.0",
            "mypy>=0.910",
        ],
        "all": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "pytest-mock>=3.6.0",
            "pytest-benchmark>=3.4.0",
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "isort>=5.10.0",
            "mypy>=0.910",
        ]
    },
    entry_points={
        "console_scripts": [
            "contextwormhole=contextwormhole.cli:main",
        ],
    },
    keywords="transformers, nlp, context, attention, huggingface, pytorch",
    project_urls={
        "Bug Reports": "https://github.com/contextwormhole/contextwormhole/issues",
        "Source": "https://github.com/contextwormhole/contextwormhole",
        "Documentation": "https://contextwormhole.readthedocs.io/",
    },
)