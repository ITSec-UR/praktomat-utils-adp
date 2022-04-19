#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import os


def limit_submissions(max_upload):
    query = "UPDATE solutions_solution SET accepted = 'f', final = 'f' WHERE number > {};".format(
        max_upload
    )
    try:
        ps_conn = psycopg2.connect(
            "host=DB_HOST port=DB_PORT dbname=DB_NAME user=DB_USER password=DB_PASS"
        )
        ps_conn.autocommit = True
        cursor = ps_conn.cursor()
        cursor.execute(query)
        cursor.close()
        ps_conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


max_uploads = (
    os.environ["PRAKTOMAT_MAX_UPLOADS"] if "PRAKTOMAT_MAX_UPLOADS" in os.environ else 3
)
limit_submissions(max_uploads)
