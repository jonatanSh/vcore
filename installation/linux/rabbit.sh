docker pull rabbitmq:3.6-management-alpine
docker run -d -p 15672:15672 -p 5672:5672 --name rabbit rabbitmq:3.6-management-alpine

