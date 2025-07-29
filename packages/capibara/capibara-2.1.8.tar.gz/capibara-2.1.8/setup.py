from setuptools import setup, find_packages
import os

# Leer el README.md desde el directorio capibara
readme_path = os.path.join("capibara", "README.md")
with open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="capibara",
    version="2.1.8",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "numpy>=1.24.0",
        "tqdm>=4.65.0",
        "datasets>=2.12.0",
        "accelerate>=0.20.0",
        "safetensors>=0.3.1",
        "einops>=0.6.1",
        "mamba-ssm>=1.0.0",
    ],
    extras_require={
        "training": [
            "wandb>=0.15.0",
            "tensorboard>=2.13.0",
            "pytorch-lightning>=2.0.0",
        ],
        "quantization": [
            "bitsandbytes>=0.41.0",
            "optimum>=1.12.0",
        ],
        "monitoring": [
            "psutil>=5.9.0",
            "prometheus-client>=0.17.0",
        ],
        "all": [
            "capibara-gpt[training]",
            "capibara-gpt[quantization]",
            "capibara-gpt[monitoring]",
        ],
    },
    python_requires=">=3.8",
    author="Anachroni s.coop",
    author_email="info@anachroni.com",
    description="Modelo de lenguaje avanzado basado en Mamba SSM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.anachroni.co",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    entry_points={
        "console_scripts": [
            "capibara=capibara.cli:main",
        ],
    },
) 