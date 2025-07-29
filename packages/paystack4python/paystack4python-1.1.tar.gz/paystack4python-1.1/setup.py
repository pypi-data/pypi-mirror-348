from setuptools import setup, find_packages
import os

def read_version():
    version_file = os.path.join(os.path.dirname(__file__), 'paystack4python', 'version.py')
    about = {}
    with open(version_file, 'r', encoding='utf-8') as f:
        exec(f.read(), about)
    return about

about = read_version()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='paystack4python',
    version=about['__version__'],
    description='Python wrapper for Paystack API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mwaiseghegift/paystack4python',
    author=about['__author__'],
    author_email='mwaiseghe.dev@gmail.com',
    license=about['__license__'],
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires=[
        'requests'
    ],
    packages=find_packages(),
    zip_safe=False
)

