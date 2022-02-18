<h1 align="center">Pytero</h1>
<h3 align="center">An updated and flexible API wrapper for the Pterodactyl API!</h3>
<p align="center"><img src="https://img.shields.io/badge/discord-invite-5865f2?style=for-the-badge&logo=discord&logoColor=white"> <img src="https://img.shields.io/badge/version-0.1.0-3572A5?style=for-the-badge"> <img src="https://img.shields.io/github/issues/PteroPackages/Pytero.svg?style=for-the-badge">

## About
Pytero is a flexible API wrapper for the Pterodactyl game panel written Python using `async`/`await` syntax. The majority of the wrapper is typed making it perfect for modern-day Python users.

## Installing
```
pip install git+https://github.com/PteroPackages/Pytero.git
```

## Getting Started
Pytero has 2 separate classes for interacting with the Application and Client API.
```python
import asyncio
from Pytero import PteroApp


# initialising the application
app = PteroApp('your.domain.here', 'pterodactyl_api_key')

# the main function
async def main():
    users = await app.users.fetch()
    [print(u) for u in users]


# run the code
asyncio.run(main())
```

This is just one of many ways to use this library!

## Contributing
Please see the [contributing guide](https://github.com/PteroPackages/Pytero/blob/main/CONTRIBUTING.md) for more.

## Contributors
- [Devonte](https://github.com/devnote-dev) - Owner, maintainer

This repository is managed under the MIT license.

© 2021-2022 PteroPackages
