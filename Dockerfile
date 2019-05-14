FROM python:2.7.15


LABEL maintainer="Christoph Schreyer <christoph.schreyer@stud.uni-regensburg.de>"


# Install required packages
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get -y install \
 cron


# Add grading scripts
COPY praktomat_limit_submissions.py /usr/local/bin/praktomat_limit_submissions.py
RUN chmod +x /usr/local/bin/praktomat_limit_submissions.py


# Setup cron
RUN sed -i "$ d" /etc/crontab
RUN echo "01 3    * * *   root    /usr/local/bin/praktomat_limit_submissions.py\n#" >> /etc/crontab
RUN cron
