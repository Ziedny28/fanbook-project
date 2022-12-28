from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb+srv://test:sparta@cluster0.40tjejk.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta
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