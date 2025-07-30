from setuptools import setup, find_packages

setup(
    name="etllog",
    version="0.1.0",
    author="Pedro Dellazzari",
    description="Logger universal com níveis customizados para ETL e automações.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "colorlog>=6.7.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
