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
    phone_number = CharField()
    stripe_id = CharField()

class Token(BaseModel):
    user_id = ForeignKeyField(User, to_field='id')
    token = CharField()
    created_at = FloatField()
    updated_at = FloatField()
    expiration_date = FloatField()

class Transaction(BaseModel):
    user_id = ForeignKeyField(User, to_field='id')
    amount = FloatField()
    bank = CharField()

class MobileCode(BaseModel):
    user_id = ForeignKeyField(User, to_field='id')
    mobile_code = CharField()

class BuyCode(BaseModel):
    user_id = ForeignKeyField(User, to_field='id')
    buy_code = CharField()
    charge_id = CharField()
    amount = CharField()

# Create the tables
User.create_table(True)
Token.create_table(True)
Transaction.create_table(True)
MobileCode.create_table(True)
BuyCode.create_table(True)

# And we connect to the DB
db.connect()
