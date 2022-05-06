import os
import configparser
from flask import jsonify
from dbConnector import dbconnector
from sqlalchemy.orm import declarative_base, sessionmaker
import sqlalchemy
from sqlalchemy import Table, create_engine, select
from sqlalchemy.ext.automap import automap_base

from dbConnector import dbconnector
 
db = dbconnector()

session = db.session

athleteTable = sqlalchemy.Table('richathletes',sqlalchemy.MetaData(),autoload=True,autoload_with=db.Engine())


temp = select(athleteTable)
with db.engine.connect() as conn:
    #print(conn.execute(temp).all())        
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

print(listOfNamesE)
print(listOfNamesC)

finalDict = {}

for dictItem in listOfNamesE:
    if dictItem in listOfNamesC:
        sum = listOfNamesE[dictItem]
        count = listOfNamesC[dictItem]
        finalDict[dictItem] = sum /count

#print(finalDict)
for eachRow in finalDict:


#Base = declarative_base()
#Base.prepare(engine, reflect=True)

#temp = Base.classes.richathletes



#Base = declarative_base()

#class sport(Base):
#    __table__ = Table('richathletes', Base.metadata, autoload=True, autoload_with=engine)



#temp = session.query(richathletes)
#print(temp)