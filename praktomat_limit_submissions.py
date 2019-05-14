#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2


def limit_submissions():
    query = ("UPDATE solutions_solution " 
	         "SET accepted = 'f', final = 'f' "
             "WHERE number > 3;")
    try:
        ps_conn = psycopg2.connect("host=DB_HOST port=DB_PORT dbname=DB_NAME user=DB_USER password=DB_PASS")
        ps_conn.autocommit = True
        cursor = ps_conn.cursor()
        cursor.execute(query)
	    cursor.close()
	    ps_conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

limit_submissions()
