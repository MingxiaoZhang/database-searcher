import mysql.connector  
import base64
import os
import io
import pandas as pd
import const
import openpyxl
import datetime

class Dbconnect:
   def __init__(self):
      # Establish mysql connection
      self.conn = mysql.connector.connect(
         user=const.USER, password=const.PASSWORD, host='localhost', database=const.DB)
      print(self.conn)
      # Get cursor from connection
      self.cursor = self.conn.cursor()

   # Upload file as binary
   def upload_file(self, table, path):
      file_name = os.path.basename(path)
      file = open(path,'rb').read()
      file = base64.b64encode(file)
      file_size = os.path.getsize(path)
      file_date = datetime.datetime.fromtimestamp(os.path.getctime(path))
      sql = """INSERT INTO """ + table + """(filename, filedata, size, date) VALUES (%s, %s, %s, %s)"""
      self.cursor.execute(sql, [file_name, file, file_size, file_date.strftime('%Y-%m-%d %H:%M:%S')])
      self.conn.commit()

   # Upload file path
   def upload_path(self, table, path):
      file_name = os.path.basename(path)
      file_size = os.path.getsize(path)
      file_date = datetime.datetime.fromtimestamp(os.path.getctime(path))
      sql = """INSERT INTO """ + table + """(filename, filepath, size, date) VALUES (%s, %s, %s, %s)"""
      self.cursor.execute(sql, [file_name, path, file_size, file_date.strftime('%Y-%m-%d %H:%M:%S')])
      self.conn.commit()

   # Search in table by name for binary file data
   def getfiles(self, field):
      query = 'SELECT * FROM ' + const.TABLE + '_1'
      self.cursor.execute(query)
      data = self.cursor.fetchall()
      return data

   # Search in table by id for binary file data
   def getfile_by_id(self, field, id):
      query = 'SELECT * FROM ' + const.TABLE + '_1' + ' WHERE ' + field + '="' + id + '"'
      self.cursor.execute(query)
      data = self.cursor.fetchall()
      return data
   
   # Decode binary file into xls file
   def getdata(self, file):
      binary_data = base64.b64decode(file)
      excel_data = pd.read_excel(io.BytesIO(binary_data))
      return excel_data

   def close(self):
      self.conn.close()