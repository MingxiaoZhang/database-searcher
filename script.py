import os
import const
from dbconnect import Dbconnect

path =r'C:\Users\micha\OneDrive\Documents\2022SpringCoop'

db = Dbconnect()
for root, dirs, files in os.walk(path):
    for file in files:
        if (file.endswith(".xlsx")):
            file_path = os.path.join(root, file)
            db.upload_file(const.TABLE + '_1', file_path)
        if (file.endswith(".rdata")):
            file_path = os.path.join(root, file)
            db.upload_path(const.TABLE + '_2', file_path)

db.close()    