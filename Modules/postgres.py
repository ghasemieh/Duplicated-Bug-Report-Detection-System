"""
-------------------------------------------------------
Duplicated Bug Report Detection
-------------------------------------------------------
Copyright (c) 2020.
Author: Alireza Ghasemieh
Email: a.ghasemieh65@gmail.com
https://github.com/ghasemieh
__Updated__ = 1/29/20, 6:35 AM.
-------------------------------------------------------
"""

import pandas as pd
import psycopg2
import os

DATABASE_HOST = os.environ.get('HOME', '127.0.0.1')
DATABASE_HOST = '192.168.188.1'


def get_connection(host=DATABASE_HOST, port='5432', user='postgres', password='password123', db_name='bug_database'):
	'''
	creates a connection to PostgreSQL database
	:param host: PostgreSQL Host address
	:param port: PostgreSQL Port
	:param user: PostgreSQL databse User
	:param password: PostgreSQL password
	:param db_name: PostgreSQL databse name
	:return: psycopg2 connection
	'''
	return psycopg2.connect(f"dbname={db_name} user={user} password={password} host={host}")


def create_table(remove_current_table=False):
	"""
		-------------------------------------------------------
		Create table using the given name if is not existed. if remove_current_table=True it first removes it and then creates a new one
		Use: create_table(table_name,remove_current_table = False)
		-------------------------------------------------------
		Returns:
			Nothing
		-------------------------------------------------------
	"""
	connection = get_connection()
	cursor = connection.cursor()
	if remove_current_table == True:
		command = "DROP TABLE IF EXISTS bug_db"
		cursor.execute(command)
	command = "CREATE TABLE IF NOT EXISTS bug_db (id INTEGER PRIMARY KEY,type TEXT, product TEXT,component TEXT,creation_time TEXT, status TEXT, priority TEXT, severity TEXT,version TEXT,summary TEXT,processed_summary TEXT, duplicates TEXT)"
	cursor.execute(command)
	connection.commit()
	connection.close()


def insert(id, type, product, component, creation_time, status, priority, severity, version, summary, processed_summary,
           duplicates):
	"""
		-------------------------------------------------------
		Insert a tuple in the given table if it is not exist.
		Use: insert(table_name, id,type,product,component,creation_time,status,priority,severity,version,summary,processed_summary)
		-------------------------------------------------------
		Returns:
			Nothing
		-------------------------------------------------------
	"""
	connection = get_connection()
	cursor = connection.cursor()
	command = "INSERT INTO bug_db VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING;"
	cursor.execute(command, (
		id, type, product, component, creation_time, status, priority, severity, version, summary, processed_summary,
		duplicates))
	connection.commit()
	connection.close()


def view():
	"""
		-------------------------------------------------------
		Extract all data from the given table
		Use: data = view(table_name)
		-------------------------------------------------------
		Returns:
			A data frame of the data
		-------------------------------------------------------
	"""
	connection = get_connection()
	cursor = connection.cursor()
	command = "SELECT * FROM bug_db"
	cursor.execute(command)
	rows = cursor.fetchall()
	connection.close()
	df = pd.DataFrame(rows, columns=["id", "type", "product", "component", "creation_time", "status",
	                                 "priority", "severity", "version", "summary", "processed_summary", "duplicates"])
	return df


def delete():
	"""
		-------------------------------------------------------
		Delete the given table
		Use: delete(table_name)
		-------------------------------------------------------
		Returns:
			Nothing
		-------------------------------------------------------
	"""
	connection = get_connection()
	cursor = connection.cursor()
	command = "DELETE FROM bug_db"
	cursor.execute(command)
	connection.commit()
	connection.close()


def extract(id):
	"""
		-------------------------------------------------------
		Extract data of the given id from the given table
		Use: data = extract(table_name, id)
		-------------------------------------------------------
		Returns:
			A data frame of the data
		-------------------------------------------------------
	"""
	connection = get_connection()
	cursor = connection.cursor()
	command = "SELECT * FROM bug_db WHERE id =" + id
	cursor.execute(command)
	rows = cursor.fetchall()
	connection.close()
	if len(rows) != 0:
		ls = list([rows[0]])
		df = pd.DataFrame(ls, columns=["id", "type", "product", "component", "creation_time", "status",
		                               "priority", "severity", "version", "summary", "processed_summary", "duplicates"])
		return df
	else:
		ls = list(rows)
		df = pd.DataFrame(ls, columns=["id", "type", "product", "component", "creation_time", "status",
		                               "priority", "severity", "version", "summary", "processed_summary", "duplicates"])
		return df

# def update_db():
#     """
#         -------------------------------------------------------
#         Update the main database
#         Use: dupdate_db()
#         -------------------------------------------------------
#         Returns:
#             Nothing
#         -------------------------------------------------------
#     """
#     connection = psycopg2.connect("dbname='bug_database' user='postgres' password='password123' host='127.0.0.1'")
#     cursor = connection.cursor()
#     cursor.execute("INSERT INTO bug_db SELECT * FROM temp_bug_db ON CONFLICT (id) DO NOTHING")
#     connection.commit()
#     connection.close()
