import mysql.connector  
import base64
import os
import io
import pandas as pd
import const
import openpyxl

def login():
   conn = mysql.connector.connect(
      user=const.USER, password=const.PASSWORD, host='localhost', database=const.DB)
   print(conn)
   #Creating a cursor object using the cursor() method
   return conn

def connect(path):
   #establishing the connection
   conn = login()
   #Creating a cursor object using the cursor() method
   cursor = conn.cursor()
   
   file_name = os.path.basename(path)
   file = open(path,'rb').read()
   file = base64.b64encode(file)
   # Preparing SQL query to INSERT a record into the database.
   sql = """INSERT INTO """ + const.TABLE + """(filename, filedata) VALUES (%s, %s)"""
   # Executing the SQL command
   cursor.execute(sql, [file_name, file])
   # Commit your changes in the database
   conn.commit()
   # Closing the connection
   conn.close()

def getfile_by_name(field, name):
   conn = login()
   cursor = conn.cursor()
   query = 'SELECT * FROM ' + const.TABLE + ' WHERE ' + field + ' LIKE "%' + name + '%"'
   cursor.execute(query)
   data = cursor.fetchall()
   return data

def getfile_by_id(field, id):
   conn = login()
   cursor = conn.cursor()
   query = 'SELECT * FROM ' + const.TABLE + ' WHERE ' + field + '="' + id + '"'
   cursor.execute(query)
   data = cursor.fetchall()
   return data
def getdata(file):
   binary_data = base64.b64decode(file)
   excel_data = pd.read_excel(io.BytesIO(binary_data))
   return excel_data
