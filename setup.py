from setuptools import setup

setup(
    name = "pyfakewebcam",
    version = "0.0.1",
    author = "John Emmons",
    author_email = "jemmons@cs.stanford.edu",
    url='https://github.com/jremmons/pyfakewebcam', 
    license='GPLv3',
    packages=['pyfakewebcam',],
    install_requires = [
        'numpy'
    ]
)
