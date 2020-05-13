from setuptools import setup, find_packages
from os import path

current_dir = path.abspath(path.dirname(__file__))

with open(path.join(current_dir, 'README.md')) as f:
    description = f.read()

setup(
    name='avaland',
    version='0.1.0-alpha',
    description='Avaland is a command-line program to download music from many sources.',
    long_description=description,
    long_description_content_type='text/markdown',
    url='https://github.com/Dragon-Born/avaland',
    download_url='https://github.com/Dragon-Born/avaland/archive/v0.1.0-alpha.tar.gz',
    keywords=[
        'Avaland',
        'Persian music', 'Persian music downloader', 'Persian music api',
        'Iranian music', 'Iranian music downloader', 'Iranian music api',
    ],
    project_urls = {
        'Documentation': 'https://github.com/dragon-born/avaland/',
        'Source': 'https://github.com/dragon-born/avaland/',
        'Tracker': 'https://github.com/dragon-born/avaland/issues',
    },
    license='MIT',
    test_suite="test",
    author='Arian Amiramjadi',
    author_email='me@arian.lol',
    packages=find_packages(),
    install_requires=['requests', 'pathlib2', 'typing'],
    scripts=['bin/avaland'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries',
        'Topic :: Multimedia :: Sound/Audio',
        'Natural Language :: English',
        'Natural Language :: Persian',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
