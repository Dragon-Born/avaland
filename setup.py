from setuptools import setup, find_packages

setup(name='Avaland Music Downloader',
      version='0.0.1',
      description='A simple cli to get WARP+ as WireGuard configuration',
      url='https://github.com/dragon-born/avaland',
      download_url='https://github.com/warp-plus/warpy-python/archive/v_05.tar.gz',
      keywords=['avaland', 'persian music downloader python', 'persian music api', 'farsi music downloader',
                "iranian music", "iranian music downloader", "farsi music API", ""],
      license='mit',
      author='Arian Amiramjadi',
      author_email='me@arian.lol',
      packages=find_packages(),
      install_requires=["requests", 'pathlib2', "typing"],
      scripts=['bin/avaland'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
          'Intended Audience :: Developers',  # Define that your audience are developers
          'Environment :: Console',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: mit License',  # Again, pick a license
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      )
