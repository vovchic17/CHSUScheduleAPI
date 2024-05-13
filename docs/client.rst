======
Client
======

Clients are used to make http requests to API server

---------------
Abstract client
---------------
Base class for all clients

.. automodule:: chsu_schedule_api.client.abc
   :members:

--------------
Aiohttp client
--------------
| Client implementation based on `aiohttp.ClientSession <https://docs.aiohttp.org/en/stable/client_reference.html#client-session>`_
| Aiohttp client is used by default in :class:`chsu_schedule_api.api.CHSUApi`

.. automodule:: chsu_schedule_api.client.aiohttp
   :members: