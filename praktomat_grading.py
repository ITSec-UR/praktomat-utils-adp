#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2

def grade_solutions():
    """ Creates attestations for all students belonging to the tutorial passed as the parameter."""

    tasks = []
    query_grade_passed = ("INSERT INTO attestation_attestation (created, public_comment, private_comment, final, published, published_on, author_id, final_grade_id, solution_id) "
                          "SELECT now(), '', '', 't', 't', now(), accounts_user.user_ptr_id, 22, solutions_solution.id "
                          "FROM accounts_user, solutions_solution, tasks_task "
                          "WHERE accounts_user.user_ptr_id = solutions_solution.author_id "
                          "AND tasks_task.id = solutions_solution.task_id "
                          "AND accounts_user.user_ptr_id = solutions_solution.author_id "
                          "AND solutions_solution.final = 't' "
                          "AND tasks_task.submission_date < now() "
                          "AND tasks_task.id = (%s) "
                          "AND NOT EXISTS (SELECT solution_id FROM attestation_attestation WHERE attestation_attestation.solution_id = solutions_solution.id); ")
    query_grade_failed = ("INSERT INTO attestation_attestation (created, public_comment, private_comment, final, published, published_on, author_id, final_grade_id, solution_id) "
                          "SELECT now(), '', '', 't', 't', now(), accounts_user.user_ptr_id, 23, MAX(solutions_solution.id) "
                          "FROM solutions_solution, accounts_user, tasks_task "
                          "WHERE solutions_solution.author_id = accounts_user.user_ptr_id "
                          "AND tasks_task.id = solutions_solution.task_id "
                          "AND tasks_task.submission_date < now() "
                          "AND tasks_task.id = (%s) "
                          "AND solutions_solution.final = 'f' "
                          "AND solutions_solution.accepted = 'f' "
                          "AND solutions_solution.author_id NOT IN (SELECT solutions_solution.author_id FROM solutions_solution WHERE accounts_user.user_ptr_id = solutions_solution.author_id AND tasks_task.id = solutions_solution.task_id AND accounts_user.user_ptr_id = solutions_solution.author_id AND solutions_solution.final = 't' AND solutions_solution.accepted = 't' AND tasks_task.id = (%s)) "
                          "AND accounts_user.user_ptr_id NOT IN (SELECT solutions_solution.author_id FROM solutions_solution, attestation_attestation WHERE solutions_solution.id = attestation_attestation.solution_id AND solutions_solution.task_id = (%s)) "
                          "GROUP BY accounts_user.user_ptr_id; ")
    query_get_tasks = ("SELECT id "
                       "FROM tasks_task "
                       "WHERE title LIKE 'H%' "
                       "OR title LIKE 'Ü%' "
                       "ORDER BY id ASC; ")

    try:
        ps_conn = psycopg2.connect("host=DB_HOST port=DB_PORT dbname=DB_NAME user=DB_USER password=DB_PASS")
        ps_conn.autocommit = True
        cursor = ps_conn.cursor()
        cursor.execute(query_get_tasks)
        task_id = cursor.fetchone()

        while task_id is not None:
            tasks += task_id
            task_id = cursor.fetchone()

        for task in tasks:
            args = (task, task, task)
            cursor.execute(query_grade_passed, args[:1])
            cursor.execute(query_grade_failed, args)

        cursor.close()
        ps_conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

grade_solutions()
