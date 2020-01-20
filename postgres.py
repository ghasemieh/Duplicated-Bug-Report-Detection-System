#  Copyright (c) 2020.
#  Alireza Ghasemieh
#  a.ghasemieh65@gmail.com
#  https://github.com/ghasemieh
# This module is responsible for connecting to postgres SQL server and handle the functions

import psycopg2

def create_table():
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE bug_report_table")
    cursor.execute("CREATE TABLE IF NOT EXISTS bug_report_table (id INTEGER,product TEXT,"
                   "component TEXT, creation_time TEXT, summary TEXT,processed_summary TEXT, status TEXT)")
    connection.commit()
    connection.close()

def insert(id,product,component,creation_time,summary,processed_summary,status):
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO bug_report_table VALUES(%s,%s,%s,%s,%s,%s,%s)",
                   (id, product, component, creation_time, summary, processed_summary, status))
    connection.commit()
    connection.close()

def view():
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bug_report_table")
    rows = cursor.fetchall()
    connection.close()
    return rows

def delete(id):
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM bug_report_table WHERE id=%s",(id,))
    connection.commit()
    connection.close()

def update(id,processed_summary):
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
    cursor = connection.cursor()
    cursor.execute("UPDATE bug_report_table SET processed_summary=%s WHERE id=%s",(processed_summary,id))
    connection.commit()
    connection.close()