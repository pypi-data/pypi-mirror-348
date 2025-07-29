from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='stx-security-filter',
    version='0.1.2',
    description='Simple Python utility to detect malicious GET input',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ajish Stephen',
    author_email='info@ajishstephen.com',
    packages=find_packages(),
    python_requires='>=3.6',
)
