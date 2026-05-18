from setuptools import setup, find_packages
import os

# Read README
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Spectra — Screen Mirror Tool"

setup(
    name="spectra-mirror",
    version="0.1.0",
    description="Mirror and control your phone screen from your PC over WiFi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="you@example.com",
    url="https://github.com/yourname/spectra",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "websockets>=11.0",
        "qrcode>=7.4",
        "Pillow>=9.0",
    ],
    extras_require={
        "fast": ["mss>=9.0"],           # faster screen capture
        "dev":  ["pytest", "black"],
    },
    entry_points={
        "console_scripts": [
            "spectra=spectra.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
    keywords="screen mirror remote control mobile phone wifi terminal",
)
