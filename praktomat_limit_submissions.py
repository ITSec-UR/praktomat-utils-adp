#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import os


def limit_submissions(conn, task, max_upload):
    query = "UPDATE solutions_solution SET accepted = 'f', final = 'f' WHERE number > {} AND task_id = {};".format(
        max_upload, task
    )
    print(query)
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_tasks(conn, regex_task):
    tasks = []
    query_get_tasks = (
        "SELECT id FROM tasks_task WHERE title SIMILAR TO '{}' ORDER BY id ASC;".format(
            regex_task
        )
    )
    try:
        cursor = conn.cursor()
        cursor.execute(query_get_tasks)
        task_id = cursor.fetchone()

        while task_id is not None:
            tasks += task_id
            task_id = cursor.fetchone()

        cursor.close()
        return tasks
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def connect_db():
    try:
        ps_conn = psycopg2.connect(
            "host=DB_HOST port=DB_PORT dbname=DB_NAME user=DB_USER password=DB_PASS"
        )
        ps_conn.autocommit = True
        return ps_conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


max_uploads = (
    os.environ["PRAKTOMAT_MAX_UPLOADS"] if "PRAKTOMAT_MAX_UPLOADS" in os.environ else 3
)
conn = connect_db()
tasks = get_tasks(conn, "(OOP|ADP): H[0-9]{2}%")
for task in tasks:
    limit_submissions(conn, task, max_uploads)
conn.close()
