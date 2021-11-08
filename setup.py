from setuptools import setup
from PteroPy import __version__


long_desc = ''
with open('./README.md') as f:
    s = f.readlines()
    long_desc = '\n'.join(s)
    del s


setup(name='pteropy',
        author='Devonte',
        url='https://github.com/devnote-dev/PteroPy',
        license='MIT',
        version=__version__,
        packages=['PteroPy'],
        description='An updated and flexible API wrapper for the Pterodactyl API!',
        long_description=long_desc,
        long_desription_content_type='text/markdown',
        include_package_data=True,
        install_requires=['aiohttp'],
        python_requires='>=3.9.0',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10'])
