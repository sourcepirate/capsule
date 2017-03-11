from setuptools import setup

def read_me():
    return open("README.md", "r").read()

install_dependencies = [
    'six',
    'PTable',
    'wget'
]

setup(
    name = 'capsule_cli',
    packages = ['capsule'],
    version = '1.0.1',
    long_description= read_me(),
    description = "Bookmark and clone your favorite code.",
    author='sourcepirate',
    author_email='plasmashadowx@gmail.com',
    url='https://github.com/sourcepirate/capsule.git',
    license="MIT",
    entry_points={
        'console_scripts': [
            'capsule=capsule:core'
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License (GPL)'
    ],
    install_requires= install_dependencies
)