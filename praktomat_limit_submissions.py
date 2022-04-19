#!/usr/bin/python3
# -*- coding: utf-8 -*-

import psycopg2
import os


def limit_submissions(conn, task, max_upload):
    query_above = "UPDATE solutions_solution SET accepted = 'f', final = 'f' WHERE number > {} AND task_id = {};".format(
        max_upload, task
    )

    query_max = "UPDATE solutions_solution SET accepted = 't', final = 't' WHERE number = {} AND task_id = {};".format(
        max_upload, task
    )
    print(query_above)
    print(query_max)
    run_sql(conn, query_above)
    run_sql(conn, query_max)


def get_tasks(conn, regex_task, rating_scale):
    query_get_tasks = "SELECT id FROM tasks_task WHERE title SIMILAR TO '{}' AND final_grade_rating_scale_id = {} ORDER BY id ASC;".format(
        regex_task, rating_scale
    )
    print(query_get_tasks)
    return run_sql(conn, query_get_tasks)


def get_rating(conn, rating_name):
    query_get_rating = "SELECT id FROM attestation_ratingscale WHERE name = '{}' ORDER BY id ASC;".format(
        rating_name
    )
    print(query_get_rating)
    rating = run_sql(conn, query_get_rating)[0][0]
    return rating


def run_sql(conn, sql):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = [record for record in cursor]

        cursor.close()
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def connect_db():
    try:
        ps_conn = psycopg2.connect(
            "host={} port={} dbname={} user={} password={}".format(
                os.environ["DB_HOST"],
                os.environ["DB_PORT"],
                os.environ["DB_NAME"],
                os.environ["DB_USER"],
                os.environ["DB_PASS"],
            )
        )
        ps_conn.autocommit = True
        return ps_conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


max_uploads = (
    os.environ["PRAKTOMAT_MAX_UPLOADS"] if "PRAKTOMAT_MAX_UPLOADS" in os.environ else 3
)
print("Run Praktomat limit homework solutions to {}".format(max_uploads))

conn = connect_db()
if not conn:
    print("No connection is established!")
    exit(1)

rating_scale = get_rating(conn, "SBL")
tasks = get_tasks(conn, "(OOP|ADP): H[0-9]{2}%", rating_scale)
for task in tasks:
    limit_submissions(conn, task[0], max_uploads)
conn.close()
