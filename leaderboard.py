import datetime
import json
import sqlite3
from flask import Flask
from flask import request
from flask import jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

app = Flask(__name__)
db = SqliteDatabase('scores.db')
db.connect()

class Score(Model):
    name = CharField()
    score = CharField()
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

if not Score.table_exists():
    db.create_tables([Score])

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/scores', methods=['GET', 'POST'])
def scores():
    if request.method == 'POST':
        username = request.form['username']
        score = request.form['score']
        try:
            Score.get_or_create(name=username, score=score, date=datetime.datetime.now())
            return "success"
        except Excetion as e:
            return "fail"
    else:
        scores = Score.select().dicts()
        return jsonify({'rows':list(scores)})