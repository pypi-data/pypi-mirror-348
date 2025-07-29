from setuptools import setup
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "modul_wrapper_readme.md").read_text(encoding='utf-8')

setup(
    name = 'Modul_Wrapper',         # How you named your package folder (MyLib)
    packages = ['Modul_Wrapper'],   # Chose the same as "name"
    version = '1.0.8',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'Control Your Library With Dictionary',   # Give a short description about your library
    long_description=long_description,            # Give a long description about your library
    long_description_content_type='text/markdown',
    author = 'KIMIN',                   # Type in your name
    author_email = 'staykimin@gmail.com',      # Type in your E-Mail
    url = 'https://github.com/staykimin/Modul-Wrapper',   # Provide either the link to your github or to your website
    # download_url = 'https://github.com/staykimin/Modul-Wrapper/archive/Modul-Wrapper-0.1.tar.gz',    # I explain this later on
    project_urls={
        'Documentation': 'https://github.com/staykimin/Modul-Wrapper',
        'Funding': 'https://github.com/staykimin/Modul-Wrapper',
        'Say Thanks!': 'https://saweria.co/staykimin',
        'Source': 'https://github.com/staykimin/Modul-Wrapper',
        'Tracker': 'https://github.com/staykimin/Modul-Wrapper/issues',
    }, 
    keywords = ['Kimin', 'Modul-Wrapper', 'J2S'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second

      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ], 
)