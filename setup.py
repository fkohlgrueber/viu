from distutils.core import setup

setup(
    name='viu',
    version='0.1.0',
    description='a small less-like Python code viewer with responsive formatting and styling',
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
    }
)