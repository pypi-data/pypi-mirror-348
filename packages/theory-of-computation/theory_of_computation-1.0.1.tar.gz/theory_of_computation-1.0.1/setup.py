from setuptools import setup, find_packages

setup(
    name='theory_of_computation',
    version='1.0.1',  # Updated version number
    packages=find_packages(),
    install_requires=[
        'colorama',
    ],
    description='A package for DFA and Turing Machine implementations.',
    long_description=open("README_for_package.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',  # Specify Markdown format for long_description
    author='Mohamed Abdelmabod',
    author_email='mohamedabdlmabod03@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
