from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="avisengine",
    version="2.0.1",
    author="AVIS Engine",
    author_email="",  # Add your contact email
    description="Python API for AVIS Engine Simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",  # Add your repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.18.3",
        "opencv-contrib-python>=4.2.0.34",
        "opencv-python>=4.2.0.34",
        "Pillow>=7.1.2",
        "PySocks>=1.7.1",
        "PyYAML>=5.3.1",
        "regex>=2020.4.4",
        "requests>=2.22.0"
    ],
)
