FROM jpetazzo/dind

RUN apt-get update -y

RUN apt-get install -y python3.5
RUN apt-get install -y python3-pip

# fix symlinks
RUN rm -f /usr/bin/python # note this is python 2
RUN rm -f /usr/bin/python3

RUN ln -s /usr/bin/python3.5 /usr/bin/python
RUN ln -s /usr/bin/python3.5 /usr/bin/python3

COPY python-req.txt /challenge_framework_build/req.txt
RUN python -m pip install -r /challenge_framework_build/req.txt

COPY entry.sh /entry.sh

# SHOULD run usng priviliged flag