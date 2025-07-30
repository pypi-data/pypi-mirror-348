from setuptools import setup, find_packages

setup(
    name="apiport",
    version="0.1.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "cryptography>=45.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "ai": ["google-generativeai>=0.3.0"],
    },
    entry_points={
        'console_scripts': [
            'apiport=apiport.cli:main',
        ],
    },
    python_requires='>=3.6',
    author="Samuel Michnik",
    author_email="michniksamuel@gmail.com",
    description="CLI tool for managing API secrets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/michniks2001/code-coffee-hack",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
