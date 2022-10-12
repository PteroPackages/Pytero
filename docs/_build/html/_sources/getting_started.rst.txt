Getting Started
===============

.. toctree::
    :maxdepth: 4

Installing
----------
Using pip:

.. code::

    pip install git+https://github.com/PteroPackages/Pytero.git

From Sources:

.. code::

    git clone https://github.com/PteroPackages/Pytero.git

Structure
---------
All of Pytero's API methods are asynchronous and make use of futures which makes use of the native
``asyncio`` library to run async programs. If you do not want to use asynchronous code for your
program, we recommend using the `Pydactyl <https://github.com/iamkubi/pydactyl>`_ API wrapper.

Application API
---------------
First, import the :class:`PteroApp` class in your file, this holds all the functions for
interacting with the application API. Make sure to also import the ``asyncio`` library (we will
need this later).

.. code:: python

    import asyncio
    from pytero import PteroApp

The class takes 2 values for initializing: your Pterodactyl panel URL, and your API key. This
supports the use of both application keys and client keys, but we recommend that you use a
client key as application keys are deprecated.

.. code:: python

    app = PteroApp('https://your.pterodactyl.domain', 'ptlc_Your_4pi_k3y')

Next, define a ``main`` function to run your program, in this example we will be fetching all users
from the API.

.. code:: python

    async def main():
        users = await app.get_users()
        for user in users:
            print(repr(user))

The ``PteroApp`` method naming convention is designed to be straightforward: all ``fetch_`` or
``get_`` methods will fetch a specific resource, all ``set_`` or ``update_`` will update a specific
resource, all ``delete_`` or ``remove_`` methods will delete a specific resource, and so on. These
methods are also documented in the :doc:`api`.

Finally, run your program with the ``asyncio.run()`` method. It's good practice to wrap the call in
a name check like below, but you can omit it for this program if you want.

.. code:: python

    if __name__ == '__main__':
        asyncio.run(main())

If you've done this correctly, you should see a list of ``User`` objects in ``repr`` form printed
to the console:

.. code::

    <User id=1 uuid=d5aa40ee-8e7f-4af5-af72-420ea383c432>
    <User id=2 uuid=66fdb4ae-2ff8-4467-95e0-65d613d11da4>
    <User id=4 uuid=e9d12be2-7bfb-419d-8888-3958a71c5cac>

The full program:

.. code:: python

    import asyncio
    from pytero import PteroApp

    app = PteroApp('https://your.pterodactyl.domain', 'ptlc_Your_4pi_k3y')

    async def main():
        users = await app.get_users()
        for user in users:
            print(repr(user))
    

    if __name__ == '__main__':
        asyncio.run(main())

..  Client API
    ----------
    TODO...

Next Steps
----------
Well done for completing this guide! Feel free to take a look at the :doc:`advanced` section for
more advanced usage of the package and API, or the :doc:`api` for more information about the
library.
