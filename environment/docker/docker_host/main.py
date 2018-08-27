from server import Server
from docker_lib import DockerHandler

server = Server(handler=DockerHandler)
server.start()

while True:
    server.handle()
