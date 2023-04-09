from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='backkr',
    version='0.0.3',
    description='A backend framework the web',
    long_description_content_type="text/markdown",
    long_description=long_description,
    author='Almas Ali',
    author_email='almaspr3@gmail.com',
    url='https://github.com/Almas-Ali/backkr',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 2 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='web framework',
    python_requires='>=3.10',

    entry_points={
        'console_scripts': [
            'backkr=backkr.cli:main',
        ],
    },
)
