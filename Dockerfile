############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
############################################################

FROM ubuntu
MAINTAINER Brad Olson<iam@brad.io>

# Add the application resources URL
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y tar git curl vim wget dialog net-tools build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip python-psycopg2

# Copy the application folder inside the container
COPY /api /srv/app/api

# Get pip to download and install requirements:
RUN pip install -r /srv/app/api/requirements.txt

# Expose ports
EXPOSE 80

# Set the default directory where CMD will execute
WORKDIR /srv/app/api

# Set the default command to execute
# when creating a new container
# i.e. using CherryPy to serve the application
CMD python server.py
