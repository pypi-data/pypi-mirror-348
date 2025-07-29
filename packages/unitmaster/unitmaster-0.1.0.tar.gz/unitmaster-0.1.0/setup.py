from setuptools import setup, find_packages

setup(
    name="unitmaster",
    version="0.1.0",
    author="Rachit Sharma, Jay Ghogale",
    author_email="rachits999003@gmail.com, jayghogale555@gmail.com",
    description="A versatile unit conversion tool",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/rachits999003/unitmasterbyrachit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "unitmaster=unitmaster.cli:main",
        ],
    },
)