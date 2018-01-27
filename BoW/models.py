from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('my_database.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField()
    password = CharField()

class Token(BaseModel):
    user_id = CharField()
    token = CharField()

class Payment(BaseModel):
    user_id = CharField()
    amount = CharField()
    bank = CharField()

# create table
User.create_table(True)
Token.create_table(True)
Payment.create_table(True)

# connect db
db.connect()
