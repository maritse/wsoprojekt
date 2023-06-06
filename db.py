# simple file to save result to the local database

# sqlite3
import sqlite3
from config import DB_PATH

def check_if_db_exists():
	try:
		conn = sqlite3.connect(DB_PATH)
		return conn
	except:
		print("Cannot connect to the library")
		return

def create_new_db():
	conn = check_if_db_exists
	cursor = conn.cursor()
	try:
		cursor.execute('''
# TODO
			''')
		cursor.commit()
		return True
	except:
		print("Failed creating of db")
		return None

def read_host_info():
	conn = check_if_db_exists()
	cursor = conn.execute("SELECT * from test;")
	for row in cursor:
		print(row)
	return cursor


def write_host_info():
	conn = check_if_db_exists()
	cursor = conn.execute("INSERT * ...")
	print("Added new data")

