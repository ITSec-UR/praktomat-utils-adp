FROM python:3.6.8


LABEL maintainer="Christoph Schreyer <christoph.schreyer@stud.uni-regensburg.de>"


# Install required packages
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install \
    python3-pip \
    && rm -r /var/lib/apt/lists/*
RUN pip3 install psycopg2


# Add required scripts
ADD ./praktomat_limit_submissions.py /
CMD python3 /praktomat_limit_submissions.py
