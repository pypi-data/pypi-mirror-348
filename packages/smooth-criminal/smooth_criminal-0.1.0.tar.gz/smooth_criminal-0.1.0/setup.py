from setuptools import setup, find_packages

setup(
    name="smooth_criminal",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21",
        "numba>=0.56",
        "tqdm>=4.60",
    ],
    entry_points={
        "console_scripts": [
            "smooth-criminal=smooth_criminal.cli:main",
        ],
    },
    author="Adolfo González",
    author_email="tu_email@example.com",
    description="Librería de aceleración automática con estilo Michael Jackson.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Alphonsus411/smooth_criminal",  # Cambia por tu URL real
    keywords="performance optimization numba numpy async michael-jackson",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.8',
)
