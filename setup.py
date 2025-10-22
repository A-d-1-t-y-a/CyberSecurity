from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="unified-memory-forensics",
    version="1.0.0",
    author="Manoj Santhoju",
    author_email="manoj.santhoju@student.ncirl.ie",
    description="A unified framework for memory forensics analysis across Windows, Linux, and macOS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/unified-memory-forensics",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "unified-forensics=unified_forensics.cli:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
