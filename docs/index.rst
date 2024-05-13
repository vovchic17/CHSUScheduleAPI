CHSUScheduleAPI
===============

**CHSUScheduleAPI** is api wrapper for `CHSU Schedule API <http://api.chsu.ru/login>`_
written in Python 3.12

.. hint::
   If you are new here, check out the :doc:`Installation guide <install>`

Features
--------
* Supports synchronous and asynchronous usage
* Has type hints
* Supports time table search by group title and lecturer name

Synchronous usage
-----------------

.. literalinclude:: ../examples/sync_usage.py

Asynchronous usage
------------------

.. literalinclude:: ../examples/async_usage.py

Contents
========
.. toctree::
   :maxdepth: 2
   
   install
   client

.. toctree::
   :maxdepth: 4

   api

.. toctree::
   :maxdepth: 2

   types
   errors