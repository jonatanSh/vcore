Containers
==========

List containers
^^^^^^^^^^^^^^^

To list all containers:

.. code-block:: python

    api.docker.containers.list()

To list only containers that are alive use:

.. code-block:: python

    api.docker.containers.list(all=True)

The response object here is a JsonResponse object (default response object)

Run
^^^

To run a new image:

.. code-block:: python

    from vcore_api.collections import PortCollection

    ports = PortCollection.create_collection()

    ports.add_tcp(123, 444) # will expose 123 as 444

    api.docker.containers.run(image="my_image", detach=True, ports=ports, command="sh /entry.sh", name="my_container"):

Shell
^^^^^
Because the environment is distributed a simple /bin/bash isn't possible

the api contains a simple shell implementation

.. note::

   this feature requires chrome

.. code-block:: python

    api.docker.shell("my_container")

.. image:: ../_static/shell.png
