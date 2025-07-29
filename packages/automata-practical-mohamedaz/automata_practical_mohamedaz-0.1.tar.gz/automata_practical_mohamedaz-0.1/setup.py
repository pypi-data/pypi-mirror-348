from setuptools import setup, find_packages

setup(
    name='automata-practical-mohamedaz',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='Mohamed Abd El-Azeem',
    description='Automata Practical Exam - DFA and Turing Machine',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
