from setuptools import setup, find_packages
import os

# Lecture des dépendances dans requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Lecture du fichier README.md pour la description longue, avec gestion d’erreur
long_description = ""
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
if os.path.isfile(readme_path):
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="face_sort",
    version="0.2.3",
    packages=find_packages(),
    install_requires=requirements,
    author="Farida Keunang Tchatchou",
    description="Un outil de tri d'images par reconnaissance faciale.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fkeunang/face_sort",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "console_scripts": [
            "face_sort=face_sort.main:face_sort",
        ],
    },
    python_requires=">=3.8",
)
