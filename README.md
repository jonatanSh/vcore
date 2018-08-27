# Challenge framework, (How to run):

Demo, upload a challenge, the framework creates a new instance and run it, connect via web 

![Demo](https://github.com/jonatanSh/challenge-framework/blob/master/github_assets/demo-run.gif)

in the above demo, first we uploaded a challenge, the system build it to a docker image, 
when we connected it ran a new container for us, and we installed vim

[old challenge framework](https://github.com/jonatanSh/challenge-framework/tree/old_framework)

# Challenge framework development (using docker, under development):

1. make sure docker, docker-compose is installed

2. head to challenge-framework/aio/development

3. run everything using main.py, for example running the framework

```python

python main.py runserver

# now head to localhost:8000 in your browser

# migrating (server must be running)

python main.py migrate

```

# Development:

1. [Build and upload base images](https://github.com/jonatanSh/challenge-framework/blob/master/environment/builder/base_images/README.md)

2. [config under environement/settings.py](https://github.com/jonatanSh/challenge-framework/blob/master/environment/settings.py)

3. run using main.py runserver -> make sure mongo and rabbitmq is running

4. deploy: deploy the indexer.py, and builder.py, then run using challenge_framework/manage.py runserver,
for loading balancing of containers compose or kubernetes.

# Challenge Processing (describe the process):

1. you upload your challenge, the system put this challenge in a queue

2. the processor process your challenge and build a docker image

3. the docker image is installed with the nodejs pluggable ssh server

4. you click play

5. the system find if a container with your challenge exists,
if not it will create one

6. the system returns the container port for the server

# Environment:

1. Builder -> the node that builds the container

2. Indexer -> the node that save the current image to the db

3. Runner -> the node that creates the container

# Demo

1. install docker, make sure docker you can execute docker without sudo

2. head to /install/linux and run install_all.sh

3. create a user using python3 main.py createsuperuser  

4. run using python3 main.py runserver

5. head to localhost:8000 in the browser, download the challenge package

6. upload your challenge

7. under the main page you'll see your challenge, click run, connect via nodejs-pluggable-server client
