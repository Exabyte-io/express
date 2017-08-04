import os

from setuptools import setup
from pip.req import parse_requirements

REQUIREMENTS_TXT = os.path.join(os.path.dirname(__file__), "requirements.txt")

setup(
    name='ExPreSS',
    version='0.1.0',
    description='Exabyte Property Ex(ss)tractor, Sourcer, Serializer class.',
    url='https://github.com/Exabyte-io/exabyte-express',
    author='Exabyte Inc.',
    author_email='info@exabyte.io',
    packages=["express"],
    install_requires=[str(i.req) for i in parse_requirements(REQUIREMENTS_TXT)],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development'
    ]
)
