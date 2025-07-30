from setuptools import setup, find_packages

setup(
    name="tea-chainquery", 
    version="0.1.2",
    packages=find_packages(),
    install_requires=["web3>=5.0.0", "click>=8.0.0", "requests>=2.0.0"],
    entry_points={"console_scripts": ["tea-chainquery=tea_chainquery.cli:cli"]},
    author="Idongesit Inyang",
    author_email="inyangidongesit22@gmail.com",
    description="ChainQuery: A CLI tool for querying blockchain data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/idyweb/chainquery",
    project_urls={"Source": "https://github.com/idyweb/chainquery"},
    license="MIT",
)