from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="qcreason",
    version="0.0.0",
    author="Alex Goessmann",
    author_email="alex.goessmann@web.de",
    description="A package for reasoning based on quantum circuits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    install_requires=[
        "qiskit>=1.2.4",
    ],
    python_requires=">=3.8",
    license="AGPL-3.0",
    url="https://github.com/algoessmann/quantum-circuit-reasoning",
    keywords="markov logic networks, tensor networks, quantum circuits"
)