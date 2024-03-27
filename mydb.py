import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = ''
)

# prepare a cursor object
cursorObject = database.cursor()

# Create a database
cursorObject.execute("CREATE DATABASE db_sistem_keuangan")

print('Create Database Done')
