# Vcore project

vcore project is a virtualization project, for dynamically creating vms, images and much more using simple python api

this project supports async tasks, such as creating the images and running them and the api is very simple.

its been deprecated from the challenge framework project the current status is work in progress. 

the backends (services) it support for now are:

  1. docker: create images, run images async.

# Purpose

The main purpose of this project is a distributed environment, with http (get/post api).

Docker api for python already exists but it doesn't support async command execution and distributed services.

This project is built on top of the existing python docker api and add this functionality.

It can be distributed easily, support easy to use http api


# Api supported languages:

1. python

2. javascript

# Api methods:

1. api.docker.images.build(directory) builds a new image (Async)

    /docker/images/build/<file_id>

    to upload a file to the server use

    /api/upload post method

2. api.docker.images.list() list images (Sync)

    /docker/query/images/list

3. api.docker.containers.list(all=False) list containers, for all containers use all=True (Sync)

    /docker/query/containers/list

    /docker/query/containers/list/alive

# Basic api (run the framework):

```python

from vcore_api import Api

# will try to connect to the vcore engine.
api = Api(host="localhost", port=5002)

# execute distrbuted remote command to build an image, path is the root directory of the docker file
request = api.docker.image.build(path)

# sync wait

while not request.is_done():
    sleep(1)

result = request.async_result()

# to use async results:

# request.request is a string that can be saved for the current session
task = api.get_task(request.request)

task.is_done() # or task.async_result() # if task is done

```