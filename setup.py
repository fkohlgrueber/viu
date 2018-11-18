from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='viu',
    version='0.0.2',
    description='A small less-like Python code viewer with responsive formatting and styling',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Felix Kohlgrüber',
    author_email='felix.kohlgrueber@gmail.com',
    url='http://github.com/fkohlgrueber/viu',
    packages=['viu'],
    install_requires=[
        'black',
        'pygments',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'viu=viu.viu:main'
        ],
    },
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
)
