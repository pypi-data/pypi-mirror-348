from setuptools import setup, find_packages

setup(
    name='tl_code',  # must be unique on PyPI
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],  # add required packages if needed
    author='NaveenTheGreat',
    description='A TL package',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
