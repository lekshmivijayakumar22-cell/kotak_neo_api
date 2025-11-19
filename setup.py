from setuptools import setup, find_packages

NAME = "neo-api-client"
VERSION = "2.0.0"
# To install the library, run the following
#
# python setup.py install


REQUIRES = [
    "bidict==0.23.1",
    "certifi==2025.10.5",
    "idna==3.11",
    "numpy==2.3.4",
    "pyjsparser==2.7.1",
    "PyJWT==2.10.1",
    "python-dateutil==2.9.0.post0",
    "python-dotenv==1.0.0",
    "requests==2.32.5",
    "six==1.17.0",
    "urllib3==2.5.0",
    "websocket-client==1.9.0",
    "websockets==15.0.1",
    "pandas==2.3.3",
    "asyncio==4.0.0",
]

setup(
    name=NAME,
    version=VERSION,
    description="Neo Trade API",
    author="ne API",
    author_email="",
    url="",
    keywords=["Neo-Trade API", "Neo Trade API's"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description="""\
    """,
)
