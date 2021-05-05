from setuptools import setup, find_packages

with open('./README.md', 'r') as f:
    long_description = f.read()

setup(
    name='express-py',
    setup_requires=['setuptools_scm'],
    use_scm_version={
        'version_scheme': 'post-release',
    },
    description='Exabyte Property Ex(ss)tractor, Sourcer, Serializer class.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Exabyte-io/exabyte-express',
    author='Exabyte Inc.',
    author_email='info@exabyte.io',
    packages=find_packages(exclude=["tests.*", "tests"]),
    install_requires=[
        "munch==2.5.0",
        "numpy>=1.19.5",
        "pymatgen==2020.4.29",
        "ase==3.17.0",
        "esse>=2020.10.19",
    ],
    extras_require={
        "test": [
            "coverage[toml]>=5.3",
            "mock>=1.3.0",
            "pyyaml>=4.2b1,<6",
        ],
    },
    python_requires=">=3.6",
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: Apache Software License'
    ]
)
