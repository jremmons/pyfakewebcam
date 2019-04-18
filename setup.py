from setuptools import setup

setup(
    name = "pyfakewebcam",
    version = "0.1.0",
    author = "John Emmons",
    author_email = "mail@johnemmons.com",
    url='https://github.com/jremmons/pyfakewebcam', 
    license='GPLv3',
    packages=['pyfakewebcam',],
    install_requires = [
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
