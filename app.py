from flask import Flask, render_template, request, redirect, url_for
from mfrc522 import SimpleMFRC522
from flask_sqlalchemy import SQLAlchemy
from RPi import GPIO as GPIO
from time import sleep
from random import randint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logider.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardid = db.Column(db.String(80), unique=True)
    schoolno = db.Column(db.String(10))
    name = db.Column(db.String(80))
    telephone = db.Column(db.String(11))
    payment = db.Column(db.Integer)

    def __init__(self, cardid, schoolno,name, telephone, payment):
        self.cardid = cardid
        self.name = name
        self.schoolno = schoolno
        self.telephone = telephone
        self.payment = payment

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardid = db.Column(db.String(80))
    date = db.Column(db.DateTime)

    def __init__(self, cardid, date):
        self.cardid = cardid
        self.date = date

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        cardid = randint(1,9999999)
        save = request.args.get("save")
        return render_template("register.html", cardid = cardid, save = save)
    else:
        newUser = User(cardid = request.form['cardid'],
                       name = request.form['name'],
                       schoolno = request.form['schoolno'],
                       telephone = request.form['telephone'],
                       payment = request.form['payment'])
        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('register', save = "ok"))

@app.route('/registers')
def registers():
    data = User.query.all()
    return render_template("registers.html", data = data)

@app.route('/delete/<id>')
def delete(id):
    data = User.query.filter_by(id=id).first()
    if data is not None:
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('registers'))
    else:
        return "Böyle Bir ID Yok!"

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        data = User.query.filter_by(id=id).first()
        return render_template("update.html", data = data)
    else:
        data = User.query.filter_by(id=id).first()
        data.cardid = request.form['cardid']
        data.name = request.form['name']
        data.schoolno = request.form['schoolno']
        data.telephone = request.form['telephone']
        data.payment = request.form['payment']

        db.session.commit()

        return redirect(url_for('update', id = id))

@app.route('/getCardId')
def getID():
    print("[*] Waiting Card")
    reader = SimpleMFRC522()
    data = reader.read()
    print("Read Card: "+str(data[0]))
    sleep(0.5)
    GPIO.cleanup()
    return redirect(url_for('register', cardid=data[0]))



if __name__ == '__main__':
    db.create_all()

    host = "127.0.0.1"
    port = 1337

    app.run(host = host, port = port, debug="on",
            #threaded=True, use_reloader=False
            )
