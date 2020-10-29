from flask import Flask,jsonify, render_template,request
from flask_cors import CORS
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import json

app=Flask(__name__)
CORS(app)

db_connection_str = 'mysql+pymysql://u831388458_covid19:Password@123@34.89.97.3:3306/u831388458_covid19stats'
db_connection = create_engine(db_connection_str)

@app.route("/meta",methods=["GET","POST"])
def get_metadata():
    query='SELECT Table_name as TablesName from information_schema.tables where table_schema = "u831388458_covid19stats";'
    df = pd.read_sql(query, con=db_connection)
    tables=df['TablesName'].tolist()
    return jsonify(tables);

@app.route('/table/<table>')
def getData(table):
    query="SELECT * FROM "+table+" LIMIT 50";
    df = pd.read_sql(query, con=db_connection)
    cols=df.columns;
    data=df.values.tolist();
    return render_template("data.html",columns=cols,data=data);

@app.route("/query")
def getTableData():
    req=request.get_json(force=True)
    query=req.get("query");
    df = pd.read_sql(query, con=db_connection)
    data=df.to_json(orient='records',indent=2)
    # data=json.loads(data)
    # data=json.dumps(data)
    return data

if(__name__=="__main__"):
    app.run(host="0.0.0.0",port=9875,debug=True)
