# Vcore project

vcore project is a virtualization project, for dynamically creating vms, images and much more using simple python api

this project supports async tasks, such as creating the images and running them and the api is very simple.

its been deprecated from the challenge framework project the current status is work in progress. 

the backends (services) it support for now are:

  1. docker: create images, run images async.
  

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

# this is a string that can be saved for the current session
task = api.get_task(request.request)

task.is_done() # or task.async_result() # if task is done

```