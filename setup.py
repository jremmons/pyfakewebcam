from setuptools import setup

setup(
    name = "pyfakewebcam",
    version = "0.1.0",
    author = "John Emmons",
    author_email = "mail@johnemmons.com",
    url='https://github.com/jremmons/pyfakewebcam', 
    license='LGPLv3',
    packages=['pyfakewebcam',],
    install_requires = [
        'numpy'
    ]
)
