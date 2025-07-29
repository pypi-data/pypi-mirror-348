from setuptools import setup, find_packages

setup(
    name='groupme-wrapper',
    version='0.1.1',
    author='Lily Groth',
    author_email='groth@u.northwestern.edu',
    description='A Python wrapper for the GroupMe API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cmajorix/groupme',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)