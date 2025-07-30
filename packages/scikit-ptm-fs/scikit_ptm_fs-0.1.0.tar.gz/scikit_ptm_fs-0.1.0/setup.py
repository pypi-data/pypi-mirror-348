from setuptools import setup, find_packages

setup(
    name='scikit-ptm-fs',
    version='0.1.0',
    author='Your Name',
    description='A Python package for integrating scikit-learn feature selection with multi-label problem transformation methods.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/scikit-ptm-fs',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.20',
        'scikit-learn>=1.0',
        'scipy>=1.5',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
