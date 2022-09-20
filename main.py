from pickle import FALSE, TRUE
from flask import Flask, render_template, request, url_for, redirect, send_file
from flask_bootstrap import Bootstrap
import const
import testdata
import altair as alt
import datapane as dp

app = Flask(__name__)
Bootstrap(app)

@app.route("/",methods =['POST','GET'])
def main():
    if request.method == "POST":
        content=dict(request.form)
        return search(content)
    return render_template("index.html", firstpage=True)

@app.route("/search",methods =['POST','GET'])
def search():
    firstpage=True
    if request.method == "POST":
        firstpage=0
        data = dict(request.form)
        files = testdata.getfile_by_name('filename', data["search"])
    else:
        files = []
    return render_template("index.html",files=files, firstpage=firstpage)

@app.route('/test.html')
def test():
    return send_file('templates/test.html')

@app.route("/display_data/<int:id>",methods =['POST','GET'])
def display(id):
    if request.method == "POST":
        data = dict(request.form)
        files = testdata.getfile_by_name('filename', data["search"])
        return render_template("index.html",files=files, firstpage=False, result=False)
    else:
        data=testdata.getfile_by_id('id', str(id))
        file=data[0][2]
        filedata=testdata.getdata(file)
        r = dp.Report(
            dp.DataTable(filedata), 
            )
        r.save(path="templates/test.html")
        dp.login(token=const.TOKEN)
        return render_template("index.html",files=[], filename=data[0][1], result=True)

if __name__ == '__main__':
	app.run(debug = False)

