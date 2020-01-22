#  Copyright (c) 2020.
#  Alireza Ghasemieh
#  a.ghasemieh65@gmail.com
#  https://github.com/ghasemieh
# This module is responsible for connecting to postgres SQL server and handle the functions

import psycopg2
import pandas as pd

def create_table():
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE bug_report_table") # Must be removed for production environment
    cursor.execute("CREATE TABLE IF NOT EXISTS bug_report_table (id INTEGER,type TEXT, product TEXT,component TEXT, "
                   "creation_time TEXT, status TEXT, priority TEXT, severity TEXT,version TEXT, "
                   "summary TEXT,processed_summary TEXT)")
    connection.commit()
    connection.close()

def insert(id,type,product,component,creation_time,status,priority,severity,version,summary,processed_summary):
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO bug_report_table VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                   (id,type,product,component,creation_time,status,priority,severity,version,summary,processed_summary))
    connection.commit()
    connection.close()

def view():
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bug_report_table")
    rows = cursor.fetchall()
    connection.close()
    df = pd.DataFrame(rows, columns=["id", "type", "product", "component", "creation_time", "status",
                                         "priority", "severity", "version", "summary", "processed_summary"])
    return df

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

def extract(id):
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bug_report_table WHERE id =%s",(id,))
    rows = cursor.fetchall()
    connection.close()
    if len(rows) != 0 :
        ls = list([rows[0]])
        df = pd.DataFrame(ls, columns=["id", "type", "product", "component", "creation_time", "status",
                                   "priority", "severity", "version", "summary", "processed_summary"])
        return df
    else:
        ls = list(rows)
        df = pd.DataFrame(ls, columns=["id", "type", "product", "component", "creation_time", "status",
                                       "priority", "severity", "version", "summary", "processed_summary"])
        return df