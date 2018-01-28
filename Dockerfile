FROM ubuntu:xenial


MAINTAINER Christoph Schreyer <christoph.schreyer@stud.uni-regensburg.de>


# Install required packages
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get -y install \
 apache2 \
 libpq-dev \ 
 zlib1g-dev \
 libmysqlclient-dev \
 libsasl2-dev \
 libssl-dev \
 swig \
 libapache2-mod-xsendfile \
 libapache2-mod-wsgi \
 openjdk-8-jdk \
 junit \
 junit4 \
 dejagnu \
 gcj-jdk \
 git-core \
 mutt
RUN apt-get -y install \
 python2.7-dev \
 python-setuptools \
 python-psycopg2 \
 python-m2crypto \
 python-pip \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
 
 
# Download & Install Praktomat
WORKDIR /var/www/
RUN git clone --recursive git://github.com/KITPraktomatTeam/Praktomat.git \
 && pip install -r Praktomat/requirements.txt

COPY local.py Praktomat/src/settings/local.py 
COPY defaults.py Praktomat/src/settings/defaults.py
COPY Builder.py Praktomat/src/checker/compiler/Builder.py 
COPY CBuilder.py Praktomat/src/checker/compiler/CBuilder.py 
COPY manage-local.py Praktomat/src/manage-local.py
 
RUN chmod 755 Praktomat/src/settings/local.py \ 
 && chmod 755 Praktomat/src/settings/defaults.py \
 && chmod 755 Praktomat/src/checker/compiler/Builder.py \
 && chmod 755 Praktomat/src/checker/compiler/CBuilder.py \
 && chmod 755 Praktomat/src/manage-local.py
 
 
# Create and initialize directories
RUN mkdir /var/www/Praktomat/PraktomatSupport /var/www/Praktomat/data \
 && ./Praktomat/src/manage-devel.py migrate --noinput
RUN ./Praktomat/src/manage-local.py collectstatic --noinput -link

 
# Set permissions for Praktomat directory
RUN adduser --disabled-password --gecos '' praktomat
RUN chmod -R 0775 Praktomat/ \
 && chown -R praktomat Praktomat/ \
 && chgrp -R praktomat Praktomat/ \
 && adduser www-data praktomat

 
# Migrate database
USER praktomat
WORKDIR /var/www
# RUN ./Praktomat/src/manage-local.py migrate --noinput
 
 
#TODO: nginx config
#TODO: kernel swap mem config
#TODO: docker setup for praktomat
#TODO: provide safe-docker-image as base image


# EXPOSE 80 443
