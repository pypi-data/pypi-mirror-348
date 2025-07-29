from setuptools import setup, find_packages
import io, os

here = os.path.abspath(os.path.dirname(__file__))

# Make sure this matches the case of your file!
long_description = io.open(os.path.join(here, "README.md"), encoding="utf-8").read()

setup(
    name="qupepfold",
    version="0.1.4",  
    author="Akshay Uttarkar",
    author_email="akshayuttarkar@gmail.com",
    description="QuPepFold: Quantum peptide folding simulations with Qiskit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/qupepfold",
    packages=find_packages(),
    include_package_data=True,            # picks up files from MANIFEST.in
    install_requires=[
        "qiskit>=0.39",
        "qiskit-aer",
        "numpy",
        "matplotlib",
        "scipy",
    ],
    entry_points={
        "console_scripts": [
            "qupepfold=qupepfold.cli:main",  # normal setuptools stub
        ],
    },
    # relative path only! no leading slash, no os.path.join here:
    scripts=["scripts/qupepfold"],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Quantum Computing",
    ],
)
