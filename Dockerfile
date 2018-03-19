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
 mutt \
 docker-engine
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

 
# Do postgres stuff (should already be set up)
# RUN psql --username=postgres \
# && CREATE USER praktomat; \
# && CREATE DATABASE praktomat_1; \
# && ALTER DATABASE praktomat_1 OWNER TO praktomat; \
# && CREATE ROLE www-data IN ROLE praktomat; \
# && \q 

# RUN ( \
# echo "" && \
# echo "local praktomat_1 praktomat trust" && \
# echo "local praktomat_1 www-data trust" ) >> /etc/postgresql/9.5/main/pg_hba.config
 
 
# Create directories
RUN mkdir -p /var/www/Praktomat/PraktomatSupport /var/www/Praktomat/data /srv/praktomat/mailsign

# Add custom config files from praktomat repository
COPY local.py Praktomat/src/settings/local.py 
COPY defaults.py Praktomat/src/settings/defaults.py
COPY Builder.py Praktomat/src/checker/compiler/Builder.py 
COPY CBuilder.py Praktomat/src/checker/compiler/CBuilder.py 
COPY manage-local.py Praktomat/src/manage-local.py
COPY createkey.py /srv/praktomat/mailsign/createkey.py
COPY safe-Dockerfile Praktomat/docker-image/Dockerfile
COPY safe-docker /usr/local/bin/safe-docker
 
RUN chmod 755 Praktomat/src/settings/local.py \ 
 && chmod 755 Praktomat/src/settings/defaults.py \
 && chmod 755 Praktomat/src/checker/compiler/Builder.py \
 && chmod 755 Praktomat/src/checker/compiler/CBuilder.py \
 && chmod 755 Praktomat/src/manage-local.py \
 && chmod 755 /srv/praktomat/mailsign/createkey.py \
 && chmod 755 Praktomat/docker-image/Dockerfile \
 && chmod 755 /usr/local/bin/safe-docker
 
 
# Migrate changes
RUN ./Praktomat/src/manage-devel.py migrate --noinput
RUN ./Praktomat/src/manage-local.py collectstatic --noinput -link


# Set permissions for Praktomat directory
RUN adduser --disabled-password --gecos '' praktomat
RUN chmod -R 0775 Praktomat/ \
 && chown -R praktomat Praktomat/ \
 && chgrp -R praktomat Praktomat/ \
 && adduser www-data praktomat

# Add mailsign
WORKDIR /srv/praktomat/mailsign/
RUN python createkey.py
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

# Docker setup
WORKDIR /var/www/Praktomat/
RUN service docker start \
 && echo -e '%praktomat ALL=NOPASSWD:ALL\npraktomat ALL=NOPASSWD:ALL\nwww-data ALL=NOPASSWD:ALL\ndeveloper ALL=NOPASSWD:ALL\npraktomat ALL= NOPASSWD: /usr/local/bin/safe-docker' | sudo EDITOR='tee -a' visudo \
 && echo -e 'www-data ALL=(TESTER)NOPASSWD:ALL\npraktomat ALL=(TESTER)NOPASSWD:ALL, NOPASSWD:/usr/local/bin/safe-docker' | sudo EDITOR='tee -a' visudo -f /etc/sudoers.d/praktomat_tester
RUN docker build -t safe-docker docker-image


#TODO: nginx config
#TODO: kernel swap mem config


EXPOSE 9002

ADD /praktomat_entrypoint.sh /
RUN chmod +x /praktomat_entrypoint.sh
ENTRYPOINT ["/praktomat_entrypoint.sh"]
