from setuptools import setup, find_packages

with open('./README.md', 'r') as f:
    long_description = f.read()

setup(
    name='express-py',
    version='2.6.0',
    description='Exabyte Property Ex(ss)tractor, Sourcer, Serializer class.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Exabyte-io/exabyte-express',
    author='Exabyte Inc.',
    author_email='info@exabyte.io',
    packages=find_packages(exclude=["tests.*", "tests"]),
    install_requires=[
        "mock==1.3.0",
        "bunch==1.0.1",
        "numpy==1.16.4",
        "xmltodict==0.9.2",
        "pymatgen==2018.5.3",
        "ase==3.17.0",
        "esse==2.3.0",
    ],
    python_requires=">=2.7,<3",
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: Apache Software License'
    ]
)
