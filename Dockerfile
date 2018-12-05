FROM python:2.7.15


LABEL maintainer="Christoph Schreyer <christoph.schreyer@stud.uni-regensburg.de>"


RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get -y install \
 cron \
 postfix \
 mailutils

COPY praktomat_grading.py /usr/local/bin/praktomat_grading.py

RUN echo -e "0 2 * * 2 root python /usr/local/bin/praktomat_grading.py\n\n" >> /etc/crontab

EXPOSE 25
