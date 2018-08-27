FROM frolvlad/alpine-python2
RUN apk update
RUN apk upgrade
RUN apk add --no-cache git bash nodejs
RUN apk add --no-cache make g++  # this is for installing node requirements
RUN git clone https://github.com/jonatanSh/gritty.git
RUN cd gritty && npm install