from setuptools import setup, find_packages
from pydrive_browser import __version__

setup(
    name='pydrive-browser',
    version=__version__,
    description='simplified file browser for pydrive.',
    long_description=open('README.md').read().strip(),
    author='Felipe Prenholato',
    author_email='philipe.rp@gmail.com',
    url='https://github.com/chronossc/pydrive-browser',
    packages=find_packages(),
    install_requires=['pydrive'],
    license='MIT License',
    zip_safe=False,
    keywords='pydrive',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
