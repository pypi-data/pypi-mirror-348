from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='face-vet',
    version='1.2.0',
    description='A package to detect fake or low-quality images using OpenCV and Tesseract',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vinayak Gaikwad',
    author_email='vinayak.gaikwad@fdplfinance.com',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'pytesseract',
        'numpy',
        'Pillow',
        'setuptools',
        'dlib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    package_data={
        "face_vet": ["models/*.dat", "models/*.xml"]
    },

    python_requires='>=3.6',
)
