from setuptools import setup, find_packages

setup(
    name='theory_of_computation',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'colorama',
    ],
    description='A package for DFA and Turing Machine implementations.',
    author='Mohamed Abdelmabod',
    author_email='mohamedabdlmabod03@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
