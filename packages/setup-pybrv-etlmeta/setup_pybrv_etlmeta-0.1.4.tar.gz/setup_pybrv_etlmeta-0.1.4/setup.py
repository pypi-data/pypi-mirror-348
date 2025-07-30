from setuptools import setup, find_packages

setup(
    name="setup_pybrv_etlmeta",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[],
    author="Ashutosh Semwal",
    author_email="info@complereinfosystem.com",
    description="A Databricks-compatible package to create etl_meta schema and rule validation tables",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ashu28555/setup_pybrv_etlmeta",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "setup_etlmeta=pybrv_etlmeta.pybrv_etlmeta:main"
        ]
    }
)
