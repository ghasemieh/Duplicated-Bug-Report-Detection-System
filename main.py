#  Copyright (c) 2020.
#  Alireza Ghasemieh
#  a.ghasemieh65@gmail.com
#  https://github.com/ghasemieh

from Bugzilla_API import API_data_extract
from text_processing import preprocessing
import pandas as pd
import sqlite as sq
import psycopg2

# # Extract data from Bugzilla website
# data_df = API_data_extract('2h')
#
# # Preprocess the data_df
# data_list = []
# for tup in data_df.itertuples():
#     processed_summary = preprocessing(data_df,tup.id,'summary')
#     data_list.append([tup.id,tup.product,tup.component,tup.creation_time,tup.summary,processed_summary,tup.status])
# new_data_df = pd.DataFrame(data_list,columns = ["id","product","component","creation_time","summary","processed_summary","status"])


# Database Functions
def create_table():
    connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='192.168.186.2' port='5432'")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE bug_report_table")
    cursor.execute("CREATE TABLE IF NOT EXISTS bug_report_table (id INTEGER,product TEXT,"
                   "component TEXT, creation_time TEXT, summary TEXT,processed_summary TEXT, status TEXT)")
    connection.commit()
    connection.close()

def insert(id,product,component,creation_time,summary,processed_summary,status):
    connection = psycopg2.connect("bug_database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO bug_report_table VALUES(?,?,?,?,?,?,?)",
                   (id,product,component,creation_time,summary,processed_summary,status))
    connection.commit()
    connection.close()

def view():
    connection = psycopg2.connect("bug_database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bug_report_table")
    rows = cursor.fetchall()
    connection.close()
    return rows

def delete(id):
    connection = psycopg2.connect("bug_database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM bug_report_table WHERE id=?",(id,))
    connection.commit()
    connection.close()

def update(id,processed_summary):
    connection = psycopg2.connect("bug_database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE bug_report_table SET processed_summary=? WHERE id=?",(processed_summary,id))
    connection.commit()
    connection.close()

# Save into a SQL database
create_table()
# for tup in new_data_df.itertuples():
#     sq.insert(tup.id,tup.product,tup.component,tup.creation_time,tup.summary,tup.processed_summary,tup.status)


# Find the n-top similar bug report

# Present on the website