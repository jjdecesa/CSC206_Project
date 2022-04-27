from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser


class dbconnector:
    def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.read('settings.conf')

        dbconnect = self.config["MYSQL"]["SQLALCHEMY_DATABASE_URI"]
        self.engine = create_engine(dbconnect, echo=True)

        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

        

    def Session(self):
        return self.session

    def Engine(self):
        return self.engine