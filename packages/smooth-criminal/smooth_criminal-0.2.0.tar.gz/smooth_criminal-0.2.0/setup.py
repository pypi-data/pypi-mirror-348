from setuptools import setup, find_packages

setup(
    name="smooth-criminal",
    version="0.2.0",
    description="⚡ Acelerador inteligente de scripts Python con estilo Michael Jackson.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Adolfo",
    author_email="tucorreo@example.com",
    url="https://github.com/Alphonsus411/smooth-criminal",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "numba",
        "rich",
        "matplotlib",
        "flet",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "smooth-criminal = smooth_criminal.cli:main"
        ]
    },
    python_requires='>=3.8',
)
