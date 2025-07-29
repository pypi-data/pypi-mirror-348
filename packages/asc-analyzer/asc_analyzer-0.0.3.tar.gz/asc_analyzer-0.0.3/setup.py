from setuptools import setup, find_packages

setup(
    name='asc-analyzer',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'spacy',
        'spacy-transformers',
        'en_core_web_trf'
    ],
    entry_points={
        'console_scripts': [
            'asc-analyzer=asc_analyzer.cli:main',
        ],
    },
    description='asc-Analyzer',
    author='Hakyung Sung',
    author_email='hksung001@gmail.com',
)
