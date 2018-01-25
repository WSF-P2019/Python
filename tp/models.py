from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('my_database.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    email = CharField()
    password = CharField()

class Post(BaseModel):
    title = CharField()
    description = CharField()

# create table
User.create_table(True)
Post.create_table(True)

# connect db
db.connect()
