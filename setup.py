"""
GROOMSAFE Setup
Behavioral Grooming Prevention & Investigator Protection Ecosystem
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="groomsafe",
    version="1.0.0",
    author="GROOMSAFE Research Team",
    author_email="contact@example.com",  # Update with actual contact
    description="Behavioral Grooming Prevention & Investigator Protection Ecosystem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/groomsafe",  # Update with actual URL
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",  # Update as needed
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
        "numpy>=1.24.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
        ],
        "production": [
            "gunicorn>=21.2.0",
            "python-multipart>=0.0.6",
            "python-json-logger>=2.0.7",
        ],
    },
    entry_points={
        "console_scripts": [
            "groomsafe-server=groomsafe.api.api:main",
        ],
    },
    include_package_data=True,
    package_data={
        "groomsafe": [
            "data/synthetic/*.json",
        ],
    },
    keywords=[
        "child-safety",
        "grooming-detection",
        "behavioral-analysis",
        "investigator-protection",
        "risk-assessment",
        "explainable-ai",
    ],
)
