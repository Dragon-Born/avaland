from setuptools import setup, find_packages

setup(
    name='avaland',
    version='0.0.1',
    description='Avaland is the best free music downloader to download music free online.',
    url='https://github.com/Dragon-Born/avaland',
    keywords=[
        'Avaland',
        'Persian music', 'Persian music downloader', 'Persian music api',
        'Iranian music', 'Iranian music downloader', 'Iranian music api',
    ],
    license='MIT',
    test_suite="test",
    author='Arian Amiramjadi',
    author_email='me@arian.lol',
    packages=find_packages(),
    install_requires=['requests', 'pathlib2', 'typing'],
    scripts=['bin/avaland'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either '3 - Alpha', '4 - Beta' or '5 - Production/Stable' as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Environment :: Console',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
