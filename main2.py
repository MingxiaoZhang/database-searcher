from pickle import FALSE, TRUE
from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
import testdata
import altair as alt
import datapane as dp

SECRET_KEY = os.urandom(32)

app = Flask(__name__)

@app.route("/",methods =['POST','GET'])
def main():
    # (C1) SEARCH FOR USERS
    if request.method == "POST":
        data = dict(request.form)
        files = testdata.getfile_by_name('test', 'test4', 'filename', data["search"])
    else:
        files = []
    return render_template("index.html",files=files)

@app.route("/display_data/<id>",methods =['POST','GET'])
def display(id):
    dp.login(token='d9464d8e2781c8c0cbdb42f886b577ee06e7b5e1')
    data=testdata.getfile_by_id('test', 'test4', 'id', id)
    print(data)
    file=data[0][2]
    filedata=testdata.getdata(file)
    print(filedata)
    r = dp.Report(
        dp.DataTable(filedata), 
        )
    r.save(path="templates/test.html")
    return render_template("index.html",files=[], result=True, link="test.html")

if __name__ == '__main__':
	app.run(debug = False)
