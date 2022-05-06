import time
from flask import Flask, render_template, request, jsonify
import os

from dbConnector import dbconnector
import sqlalchemy
from sqlalchemy import Table, create_engine, select
from sqlalchemy.orm import sessionmaker

import matplotlib.pyplot as plt
import numpy as np

from collections import Counter

appdb = Flask(__name__)
appdb.config['UPLOAD_FOLDER'] = '/static' 

def dbStuff():
    db = dbconnector()
    session = db.session

    athleteTable = sqlalchemy.Table('richathletes',sqlalchemy.MetaData(),autoload=True,autoload_with=db.Engine())

    temp = select(athleteTable)
    with db.engine.connect() as conn:        
        results = conn.execute(temp).all()
    athlete_list = [r._asdict() for r in results]

    for e in athlete_list:
        e['sport'] = e['sport'].capitalize()
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
        item['sport'] = item['sport'].capitalize()
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
        e['sport'] = e['sport'].capitalize()
        temp = e['prevyearrank']
        if not temp:
            e['prevyearrank'] = "n/a" 
        e['earnings'] = float(e['earnings'])
        if e['currentrank'] == 1:
            finalDict.append(e)
        

    
    


    return finalDict

def dbStuffAVGNat():
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
        if item['nationality'] not in listOfNamesE:
            listOfNamesE[item['nationality']] = 0
            listOfNamesC[item['nationality']] = 0
        listOfNamesE[item['nationality']] += float((item['earnings']))
        listOfNamesC[item['nationality']] += 1

    print(listOfNamesE)
    print(listOfNamesC)
    finalDict = {}

    for dictItem in listOfNamesE:
        if dictItem in listOfNamesC:
            sum = listOfNamesE[dictItem]
            count = listOfNamesC[dictItem]
            finalDict[dictItem] = sum /count

    return finalDict

def dbStuffEachNat():
    db = dbconnector()
    session = db.session

    athleteTable = sqlalchemy.Table('richathletes',sqlalchemy.MetaData(),autoload=True,autoload_with=db.Engine())

    temp = select(athleteTable)
    with db.engine.connect() as conn:        
        results = conn.execute(temp).all()
    tempList = np.array(results)

    nat = []

    for item in tempList[:,1]:
        nat.append(item)

    finalDict = Counter(nat)

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


@appdb.route('/avgGraph/', methods = ['get'])
def avgGraph():
    tempText = dbStuffAVG()
    data = [[],[]]

    for ea in tempText:
        data[0].append(ea)
        data[1].append(tempText[ea])

    plt.figure().clear()
    plt.bar(data[0], data[1])

    plt.xticks(rotation=90)
    plt.gcf().subplots_adjust(bottom=0.475)
    plt.title('Average Earnings')
    plt.ylabel('In Millions')

    plt.savefig('static/avgGraph.png',dpi=150)
    full_filename = os.path.join(appdb.config['UPLOAD_FOLDER'], 'avgGraph.png')
    return render_template('databaseAvgGraph.html',userImage = full_filename)

@appdb.route('/avgNat/', methods = ['get'])
def avgNat():
    tempText = dbStuffAVGNat()
    data = [[],[]]

    for ea in tempText:
        data[0].append(ea)
        data[1].append(tempText[ea])

    plt.figure().clear()
    plt.bar(data[0], data[1])

    plt.xticks(rotation=90)
    plt.gcf().subplots_adjust(bottom=0.475)
    plt.title('Average Earnings')
    plt.ylabel('In Millions')

    plt.savefig('static/avgNat.png',dpi=150)
    full_filename = os.path.join(appdb.config['UPLOAD_FOLDER'], 'avgNat.png')
    return render_template('databaseAvgNat.html',userImage = full_filename)

@appdb.route('/eachNat/', methods = ['get'])
def eachNat():
    tempText = dbStuffEachNat()
    datax = []
    datay = []

    for ea in tempText:
        datax.append(ea)
        datay.append(tempText[ea])

    plt.figure().clear()
    plt.bar(datax, datay)

    plt.xticks(rotation=90)
    plt.gcf().subplots_adjust(bottom=0.275)
    plt.title('Number of players from each country')

    for i in range(len(datax)):
        plt.text(i,datay[i],datay[i],ha='center')

    plt.savefig('static/eachNat.png',dpi=150)
    full_filename = os.path.join(appdb.config['UPLOAD_FOLDER'], 'eachNat.png')
    return render_template('databaseeachNat.html',userImage = full_filename)

if __name__ == '__main__':
    appdb.run(debug=True)

##python "appdb.py" //to run it




