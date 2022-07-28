<h1 align="center">Pytero</h1>
<h3 align="center">A flexible API wrapper for Pterodactyl in Python</h3>
<p align="center"><a href="https://discord.com/invite/dwcfTjgn7S" type="_blank"><img src="https://img.shields.io/badge/discord-invite-5865f2?style=for-the-badge&logo=discord&logoColor=white"></a> <img src="https://img.shields.io/badge/version-0.1.0-3572A5?style=for-the-badge"> <img src="https://img.shields.io/github/issues/PteroPackages/Pytero.svg?style=for-the-badge"></p>

## About
Pytero is a flexible API wrapper for the [Pterodactyl Game Panel](https://pterodactyl.io) written Python using `async`/`await` syntax and up-to-date typings for proper type-checker support.

## Installing
```
pip install git+https://github.com/PteroPackages/Pytero.git
```

## Getting Started

### Using the Application API
```python
import asyncio
from pytero import PteroApp


# initialize the application
app = PteroApp('your.domain.name', 'pterodactyl_api_key')

async def main():
    # get all servers
    servers = await app.get_servers()
    for server in servers:
        print(server)


# run the function
asyncio.run(main())
```

### Using the Client API
```python
from pytero import PteroClient


# initialize the client
client = PteroClient('your.domain.name', 'pterodactyl_api_key')
# create the websocket shard
shard = client.create_shard('280e5b1d')

# listen for status updates
@shard.event
def on_status_update(status):
    print('server %s status: %s' % (shard.identifier, status))


# launch the shard
shard.launch()
```

## Contributing
Please see the [contributing guide](https://github.com/PteroPackages/Pytero/blob/main/CONTRIBUTING.md) for more.

## Contributors
- [Devonte](https://github.com/devnote-dev) - Owner, maintainer

This repository is managed under the MIT license.

© 2021-2022 PteroPackages
