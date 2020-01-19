#  Copyright (c) 2020.
#  Alireza Ghasemieh
#  a.ghasemieh65@gmail.com
#  https://github.com/ghasemieh

import sqlite3

# Database Functions
def create_table():
    connection = sqlite3.connect("bug_database.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE bug_report_table")
    cursor.execute("CREATE TABLE IF NOT EXISTS bug_report_table (id INTEGER,product TEXT,"
                   "component TEXT, creation_time TEXT, summary TEXT,processed_summary TEXT, status TEXT)")
    connection.commit()
    connection.close()

def insert(id,product,component,creation_time,summary,processed_summary,status):
    connection = sqlite3.connect("bug_database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO bug_report_table VALUES(?,?,?,?,?,?,?)",
                   (id,product,component,creation_time,summary,processed_summary,status))
    connection.commit()
    connection.close()

def view():
    connection = sqlite3.connect("bug_database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bug_report_table")
    rows = cursor.fetchall()
    connection.close()
    return rows

def delete(id):
    connection = sqlite3.connect("bug_database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM bug_report_table WHERE id=?",(id,))
    connection.commit()
    connection.close()

def update(id,processed_summary):
    connection = sqlite3.connect("bug_database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE bug_report_table SET processed_summary=? WHERE id=?",(processed_summary,id))
    connection.commit()
    connection.close()