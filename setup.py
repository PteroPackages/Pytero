'''# Pytero
A flexible API wrapper for the Pterodactyl API

Author: Devonte W <https://github.com/devnote-dev>
Repository: https://github.com/PteroPackages/Pytero
License: MIT

© 2021-present PteroPackages
'''

from setuptools import setup
from pytero import __version__


with open('./README.md', encoding='utf-8') as file:
    LONG_DESC = '\n'.join(file.readlines())
    file.close()


setup(
    name='pytero',
    author='Devonte W',
    url='https://github.com/PteroPackages/Pytero',
    license='MIT',
    version=__version__,
    packages=['pytero'],
    description='A flexible API wrapper for Pterodactyl in Python',
    long_description=LONG_DESC,
    long_desription_content_type='text/markdown',
    include_package_data=True,
    install_requires=['aiohttp'],
    python_requires='>=3.10.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10'
    ]
)
