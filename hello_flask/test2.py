import matplotlib.pyplot as plt
import numpy as np

import time
from flask import Flask, render_template, request, jsonify

from dbConnector import dbconnector
import sqlalchemy
from sqlalchemy import Table, create_engine, select
from sqlalchemy.orm import sessionmaker

from collections import Counter

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

plt.savefig('static/test.png')
