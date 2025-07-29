from setuptools import setup, find_packages

setup(
    name="custom-csv-tool",  # PyPI name (can include dashes)
    version="0.1.0",
    description="Custom CrewAI tool for reading and analyzing CSVs from Azure Blob.",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "pydantic",
        "crewai",
        "python-dotenv",
        "azure-storage-blob"
    ],
    python_requires=">=3.7",
)
