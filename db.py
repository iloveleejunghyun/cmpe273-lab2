import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import json

DATABASE = 'mydb.db'

######################################################################################################################################


def init_db():
    #create database and tables
    
    sqliteDB = sqlite3.connect(DATABASE)
    print ("Opened database successfully")

    #sqliteDB.execute('DROP TABLE IF exists student')
    sqliteDB.execute('CREATE TABLE IF NOT EXISTS student (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, addr TEXT, city TEXT)')

    #sqliteDB.execute('DROP TABLE IF exists clazz')
    sqliteDB.execute('CREATE TABLE IF NOT EXISTS clazz (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')

    #sqliteDB.execute('DROP TABLE IF exists classstudent')
    sqliteDB.execute('CREATE TABLE IF NOT EXISTS classstudent (id INTEGER PRIMARY KEY AUTOINCREMENT, class_id INTEGER, student_id INTEGER)')

    print ("Tables created successfully")


init_db()