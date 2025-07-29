from setuptools import setup, find_packages

setup(
    name='dxplorer',  
    version='0.1.0',
    author='Talha Sarfraz',
    author_email='talhasarfraz29@gmail.com',
    description='A Python package for quick data quality profiling with visualization and imputation suggestions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/talha-11-11/dxplorer',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas',
        'seaborn',
        'matplotlib',
    ],
)
