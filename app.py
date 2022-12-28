import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/homework", methods=["POST"])
def homework_post():
    name_recive = request.form['name_give']
    comment_recive = request.form['comment_give']
    time_now = datetime.now()
    day = time_now.strftime("%A")
    date = time_now.strftime("%d")
    month = time_now.strftime("%B")
    year = time_now.strftime("%Y")
    time = day + ', ' + date + ' ' + month + ' ' + year
    
    doc = {
        'name':name_recive,
        'comment':comment_recive,
        'time' : time
    }
    db.fanmessages.insert_one(doc)
    return jsonify({'msg':'POST request!'})

@app.route("/homework", methods=["GET"])
def homework_get():
    message_list = list(db.fanmessages.find({},{'_id':False}))
    return jsonify({'messages':message_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)