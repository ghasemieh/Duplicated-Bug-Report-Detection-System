#  Copyright (c) 2020.
#  Alireza Ghasemieh
#  a.ghasemieh65@gmail.com
#  https://github.com/ghasemieh
# This module is responsible for connecting to postgres SQL server and handle the functions

import psycopg2
import pandas as pd

def create_table(table_name,remove_current_table = False):
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
    cursor = connection.cursor()
    if remove_current_table == True:
        command = "DROP TABLE IF EXISTS " + table_name
        cursor.execute(command)
    command = "CREATE TABLE IF NOT EXISTS " + table_name + " (id INTEGER PRIMARY KEY,type TEXT, product TEXT,component TEXT,creation_time TEXT, status TEXT, priority TEXT, severity TEXT,version TEXT,summary TEXT,processed_summary TEXT)"
    cursor.execute(command)
    connection.commit()
    connection.close()

def insert(table_name, id,type,product,component,creation_time,status,priority,severity,version,summary,processed_summary):
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
    cursor = connection.cursor()
    command = "INSERT INTO " + table_name + " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING;"
    cursor.execute(command,(id,type,product,component,creation_time,status,priority,severity,version,summary,processed_summary))
    connection.commit()
    connection.close()

def update_db():
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO bug_db SELECT * FROM temp_bug_db ON CONFLICT (id) DO NOTHING")
    connection.commit()
    connection.close()


def view(table_name):
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
    cursor = connection.cursor()
    command = "SELECT * FROM " + table_name
    cursor.execute(command)
    rows = cursor.fetchall()
    connection.close()
    df = pd.DataFrame(rows, columns=["id", "type", "product", "component", "creation_time", "status",
                                         "priority", "severity", "version", "summary", "processed_summary"])
    return df

def delete(table_name):
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
    cursor = connection.cursor()
    command = "DELETE FROM " + table_name
    cursor.execute(command)
    connection.commit()
    connection.close()

# def update(id,processed_summary):
#     connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
#     cursor = connection.cursor()
#     cursor.execute("UPDATE bug_report_table SET processed_summary=%s WHERE id=%s",(processed_summary,id))
#     connection.commit()
#     connection.close()

def extract(table_name, id):
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1' port='5432'")
    cursor = connection.cursor()
    command = "SELECT * FROM " +table_name + " WHERE id ="+id
    cursor.execute(command)
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