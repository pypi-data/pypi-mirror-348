from setuptools import setup, find_packages

import io
with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="ciphercrackerMSWA02",
    version="0.1.4",
    package_dir={"": "src"},
    py_modules=["cipherCracker"],
    author="Oskar Šefců et al.",
    author_email="oskysef@gmail.com",
    description="monoalphabetic substitution cipher cracking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    include_package_data=True,               # key to include MANIFEST files
    package_data={                           # fallback for non-.py files
        "ciphercrackerMSWA02": ["data/*.txt"],
    },
    url="https://github.com/MSWA-02/python_semestral.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
