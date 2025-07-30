# Este archivo es el núcleo de la configuración para empaquetar y distribuir la librería en Python.
from setuptools import setup, find_packages
# para manipular rutas de archivos de forma moderna y segura.
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="lib_rr",  # Replace with your library name
    version="0.2.2",  # Initial version
    author="Jorge Rodriguez",  # Replace with your name
    author_email="jarodriguezcastano@ucundinamarca.edu.co",  # Replace with your email
    description="A test library",  # Short description
    long_description=long_description,  # Long description from README.md
    long_description_content_type="text/markdown",
    url="https://github.com/JorgeRodriguez9/lib_rr",  # Replace with your GitHub repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Replace with your license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[

    "numpy"

    ],
)