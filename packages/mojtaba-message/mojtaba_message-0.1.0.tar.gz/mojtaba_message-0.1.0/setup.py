from setuptools import setup, find_packages

setup(
    name='mojtaba-message',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    description='A simple message package by Mojtaba',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your@email.com',
    url='https://github.com/yourusername/mojtaba-message',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
