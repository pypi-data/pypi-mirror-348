from setuptools import setup, find_packages

setup(
    name="coragem",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["web3>=5.0.0", "click>=8.0.0", "requests>=2.0.0"],
    entry_points={"console_scripts": ["coragem=coragem.cli:cli"]},
    author="Idongesit Inyang",
    author_email="inyangidongesit22@gmail.com",
    description="Coragem: A CLI tool for querying blockchain data", 
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/idyweb/coragem", 
    project_urls={"Source": "https://github.com/idyweb/coragem"},
    license="MIT",
)