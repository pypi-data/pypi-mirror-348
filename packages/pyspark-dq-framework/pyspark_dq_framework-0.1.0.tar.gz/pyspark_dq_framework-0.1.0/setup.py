# setup.py
from setuptools import setup, find_packages

setup(
    name='pyspark-dq-framework',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A PySpark-based Data Quality Framework using YAML-configurable checks.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/pyspark-dq-framework',  # Replace with your GitHub repo
    packages=find_packages(),
    install_requires=[
        'pyspark>=3.0.0',
        'pyyaml'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ],
    python_requires='>=3.7',
    include_package_data=True
)
