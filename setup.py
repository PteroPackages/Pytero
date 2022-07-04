from setuptools import setup, find_packages
from Pytero import __version__


with open('./README.md') as file:
    long_desc = '\n'.join(file.readlines())
    file.close()


setup(
    name='Pytero',
    author='Devonte',
    url='https://github.com/PteroPackages/Pytero',
    license='MIT',
    version=__version__,
    packages=find_packages('Pytero'),
    description='A flexible API wrapper for the Pterodactyl API',
    long_description=long_desc,
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
