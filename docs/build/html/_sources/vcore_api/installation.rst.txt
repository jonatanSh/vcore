Setup
=====
Installation:
^^^^^^^^^^^^^

To install the python api package use pip

.. code-block:: bash

    pip install vcore_api

Additional dependencies (optional):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* chrome (optional, gui function use chrome as a renderer)

Connect to the vcore engine
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from vcore_api import Api

    api = Api(host="localhost", port=5002) # defaults are localhost, 5002

