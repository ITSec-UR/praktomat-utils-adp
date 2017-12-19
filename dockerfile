FROM ubuntu:xenial


MAINTAINER Christoph Schreyer <christoph.schreyer@stud.uni-regensburg.de>


# Install required packages
RUN apt-get update \
 && apt-get install postgresql-9.5 apache2 libpq-dev zlib1g-dev libmysqlclient-dev libsasl2-dev libssl-dev swig libapache2-mod-xsendfile libapache2-mod-wsgi sun-java6-jdk junit junit4 dejagnu gcj-jdk git-core mutt \
 && apt-get install python2.7-dev python-setuptools python-psycopg2 python-m2crypto \
 && rm -rf /var/lib/apt/lists/*
 
 
# Download & Install Praktomat
WORKDIR /var/www
RUN git clone --recursive git://github.com/KITPraktomatTeam/Praktomat.git \
 && pip install -r Praktomat/requirements.txt

 
# Create Praktomat postgres user and database
RUN sudo -u postgres createuser -DRS praktomat \
 && sudo -u postgres createdb -O praktomat praktomat_1

 
# Edit postgres config
RUN ( \
 echo "" && \
 echo "LOCAL PRAKTOMAT_1 PRAKTOMAT TRUST" && \
 echo "LOCAL PRAKTOMAT_1 WWW-DATA TRUST" ) >> /etc/postgresql/9.5/main/pg_hba.config
 
 
# Create the postgres role
RUN sudo -u postgres psql praktomat_1 \
 && CREATE ROLE "www-data" IN ROLE praktomat;

 
# Add custom config files from repository
COPY local.py /var/www/Praktomat/src/settings/local.py \
 && default.py /var/www/Praktomat/src/settings/default.py \
 && Builder.py /var/www/Praktomat/src/checker/compiler/Builder.py \
 && CBuilder.py /var/www/Praktomat/src/checker/compiler/CBuilder.py
 # TODO ******* check required permissions*********
RUN chmod /var/www/Praktomat/src/settings/local.py \ 
 && chmod /var/www/Praktomat/src/settings/default.py \
 && chmod /var/www/Praktomat/src/checker/compiler/Builder.py \
 && chmod /var/www/Praktomat/src/checker/compiler/CBuilder.py

 
 
# Create and initialize directories
RUN mkdir /var/www/Praktomat/PraktomatSupport /var/www/Praktomat/data \
 && ./Praktomat/src/manage-devel.py migrate --noinput \
 && ./Praktomat/src/manage-local.py collectstatic --noinput -link

 
# Set permissions for Praktomat directory
RUN chmod -R 0775 Praktomat/ \
 && chown -R praktomat Praktomat/ \
 && chgrp -R praktomat Praktomat/ \
 && adduser www-data praktomat

 
# Migrate database
USER praktomat
RUN ./Praktomat/src/manage-local.py migrate --noinput \
 && ./Praktomat/src/manage-local-py createsuperuser \
 && ./Praktomat/src/manage-local.py runserver


EXPOSE 80 443