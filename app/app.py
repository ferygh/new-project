from flask import Flask , request
from flask import jsonify
import json
import pymysql
import subprocess
conn= pymysql.connect("localhost","root","PASSWD","reports")
x=conn.cursor()
sql = """SELECT * FROM wether ORDER BY id DESC LIMIT 1"""

x.execute(sql)
app = Flask(__name__)


@app.route("/temprature", methods=['GET'])
def hello():
    x.execute(sql)
    row_headers=[i[0] for i in x.description] #this will extract row headers
    rv = x.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data)
     

@app.route('/temprature', methods=['POST'])
def set_temprature():
    temprature = request.json.get('temprature', "")
    wind = request.json.get('wind', "")
    sql = "INSERT INTO wether(temprature, wind) VALUES(%s, %s)"
    data = (temprature,wind)
    print(data)
    x.execute(sql, data)
    conn.commit()

@app.route('/cpu')
def cpu():
    output = subprocess.Popen(["uptime"],stdout=subprocess.PIPE)
    response = output.communicate()
    return (response)

if __name__ == '__main__':
     app.run(host='0.0.0.0')
