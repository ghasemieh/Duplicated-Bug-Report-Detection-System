#  Copyright (c) 2020.
#  Alireza Ghasemieh
#  a.ghasemieh65@gmail.com
#  https://github.com/ghasemieh

from Bugzilla_API import API_data_extract
from text_processing import preprocessing
import pandas as pd
import sqlite3

# Extract data from Bugzilla website
data_df = API_data_extract('2h')

# Preprocess the data_df
data_list = []
for tup in data_df.itertuples():
    processed_summary = preprocessing(data_df,tup.id,'summary')
    data_list.append([tup.id,tup.product,tup.component,tup.creation_time,tup.summary,processed_summary,tup.status])
new_data_df = pd.DataFrame(data_list,columns = ["id","product","component","creation_time","summary","processed_summary","status"])


# Create db if not exist
def create_table():
    connection = sqlite3.connect("bug_database.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS bug_report_table (summary TEXT,	component TEXT,	"
               "status TEXT, id INTEGER, creation_time TEXT, product TEXT, processed_summary TEXT )")
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


# Save into a SQL database
# create_table()
# for tup in new_data_df.itertuples():
#     insert(tup.id,tup.product,tup.component,tup.creation_time,tup.summary,tup.processed_summary,tup.status)

# Find the n-top similar bug report

# Present on the website