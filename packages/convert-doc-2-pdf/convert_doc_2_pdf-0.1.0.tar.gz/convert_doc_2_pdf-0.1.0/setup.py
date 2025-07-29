from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="convert_doc_2_pdf",
    version="0.1.0",
    author="Swati",
    author_email="your.email@example.com",
    description="Convert Microsoft Word documents (.doc, .docx) to PDF format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/doc2pdf",
    # project_urls={
    #     "Bug Tracker": "https://github.com/yourusername/doc2pdf/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "docx2pdf>=0.1.7",
    ],
    entry_points={
        "console_scripts": [
            "doc2pdf=doc2pdf.cli:main",
        ],
    },
)