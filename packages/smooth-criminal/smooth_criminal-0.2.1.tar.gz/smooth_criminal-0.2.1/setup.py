from setuptools import setup, find_packages

setup(
    name="smooth_criminal",
    version="0.2.1",
    author="Adolfo González",
    author_email="tucorreo@example.com",
    description="Dashboard de análisis de rendimiento con decoradores inteligentes",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Alphonsus411/smooth_criminal",  # Cambiar si aplica
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flet>=0.19.0",
        "pandas",
        "tabulate",
        "matplotlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
