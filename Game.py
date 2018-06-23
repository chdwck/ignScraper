from peewee import *
from config import DBNAME, DBUSER, DBPASS

db = MySQLDatabase(DBNAME, user=DBUSER, passwd=DBPASS)

class Game(Model):
    name = TextField()
    score = FloatField()
    oneword = CharField()
    description = TextField()
    url = TextField()

    class Meta:
        database = db

    @staticmethod
    def close():
        db.close()

    @staticmethod
    def connect():
        db.connect()