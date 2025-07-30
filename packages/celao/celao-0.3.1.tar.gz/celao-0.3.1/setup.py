from setuptools import setup, find_packages

setup(
    name="CELAO",
    version="0.3.1",
    author="Good",
    packages=find_packages(include=['celao', 'celao.*', 'lib', 'lib.*']),
    description="Visualization tool for correlation n-ptychs of linguistic attributes",
    url="https://github.com/Good03/celao/",
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "networkx",
        "gensim"
    ]
)