import os
import const
from dbconnect import Dbconnect

path =r'C:\Users\micha\OneDrive\Documents\2022SpringCoop'

db = Dbconnect()
for root, dirs, files in os.walk(path):
    for file in files:
        if (file.endswith(".txt")):
            file_path = os.path.join(root, file)
            db.upload_path(const.TABLE + '_2', file_path)

db.close()    