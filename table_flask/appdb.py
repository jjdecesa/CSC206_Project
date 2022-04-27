import time
from flask import Flask, render_template, request, jsonify

from dbConnector import dbconnector
import sqlalchemy
from sqlalchemy import Table, create_engine, select
from sqlalchemy.orm import sessionmaker

appdb = Flask(__name__)

def dbStuff():
    db = dbconnector()
    session = db.session

    athleteTable = sqlalchemy.Table('richathletes',sqlalchemy.MetaData(),autoload=True,autoload_with=db.Engine())

    temp = select(athleteTable)
    with db.engine.connect() as conn:        
        results = conn.execute(temp).all()
    athlete_list = [r._asdict() for r in results]

    for e in athlete_list:
        temp = e['prevyearrank']
        if not temp:
            e['prevyearrank'] = "n/a" 
        e['earnings'] = float(e['earnings'])


    return athlete_list

def dbStuffAVG():
    db = dbconnector()
    session = db.session

    athleteTable = sqlalchemy.Table('richathletes',sqlalchemy.MetaData(),autoload=True,autoload_with=db.Engine())

    temp = select(athleteTable)
    with db.engine.connect() as conn:        
        results = conn.execute(temp).all()
    tempList = [r._asdict() for r in results]

    listOfNamesE = {}
    listOfNamesC = {}

    for item in tempList:
        if item['sport'] not in listOfNamesE:
            listOfNamesE[item['sport']] = 0
            listOfNamesC[item['sport']] = 0
        listOfNamesE[item['sport']] += float((item['earnings']))
        listOfNamesC[item['sport']] += 1

    finalDict = {}

    for dictItem in listOfNamesE:
        if dictItem in listOfNamesC:
            sum = listOfNamesE[dictItem]
            count = listOfNamesC[dictItem]
            finalDict[dictItem] = sum /count

    return finalDict

def dbStuffTop():
    db = dbconnector()
    session = db.session

    athleteTable = sqlalchemy.Table('richathletes',sqlalchemy.MetaData(),autoload=True,autoload_with=db.Engine())

    temp = select(athleteTable)
    with db.engine.connect() as conn:        
        results = conn.execute(temp).all()
    athlete_list = [r._asdict() for r in results]

    finalDict = []

    for e in athlete_list:
        temp = e['prevyearrank']
        if not temp:
            e['prevyearrank'] = "n/a" 
        e['earnings'] = float(e['earnings'])
        if e['currentrank'] == 1:
            finalDict.append(e)
        

    
    


    return finalDict


@appdb.route('/', methods = ['get'])
def dbRoute():


    tempText = dbStuff()


    #return tempText
    return render_template('database.html', al=tempText)


@appdb.route('/ranks/', methods = ['get'])
def ranks():


    tempText = dbStuff()


    #return tempText
    return render_template('databaseRanks.html', al=tempText)

@appdb.route('/avg/', methods = ['get'])
def avg():

    tempText = dbStuffAVG()

    return render_template('databaseAVG.html', al=tempText)

    
@appdb.route('/top/', methods = ['get'])
def top():

    tempText = dbStuffTop()

    return render_template('databaseTop.html', al=tempText)


if __name__ == '__main__':
    appdb.run(debug=True)

##python "appdb.py" //to run it




