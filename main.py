from pickle import FALSE, TRUE
from flask import Flask, render_template, request, url_for, redirect, send_file
from flask_bootstrap import Bootstrap
import const
from dbconnect import Dbconnect
import altair as alt
import datapane as dp

app = Flask(__name__)
Bootstrap(app)

@app.route("/",methods =['POST','GET'])
def main():
    # Connect to db
    db = Dbconnect()
    files = db.getfiles('filename')
    return render_template("index.html",files=files)

@app.route('/test.html')
def test():
    return send_file('templates/test.html')

@app.route("/display_data/<int:id>",methods =['POST','GET'])
def display(id):
    db = Dbconnect()
    # Find row by url id
    data=db.getfile_by_id('id', str(id))
    # Get file data in third column
    file=data[0][2]
    # Decode binary data into dataframe
    filedata=db.getdata(file)
    # Generate datapane report
    r = dp.Report(
        dp.DataTable(filedata), 
        )
    # Create temporary page for viewing
    r.save(path="templates/test.html")
    dp.login(token=const.TOKEN)
    return render_template("view.html")

if __name__ == '__main__':
	app.run(debug = False)

