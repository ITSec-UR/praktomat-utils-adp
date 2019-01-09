FROM python:2.7.15


LABEL maintainer="Christoph Schreyer <christoph.schreyer@stud.uni-regensburg.de>"


# Install required packages
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get -y install \
 cron \
 postfix \
 mailutils


# Add grading scripts
COPY praktomat_grading.py /usr/local/bin/praktomat_grading.py
RUN chmod +x /usr/local/bin/praktomat_grading.py


# Setup cron
RUN echo "01 3    * * 2   root    /usr/local/bin/praktomat_grading.py\n#" >> /etc/crontab
RUN cron


EXPOSE 25
