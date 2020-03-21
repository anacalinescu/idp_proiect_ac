from typing import List, Dict
from flask import Flask
from flask import request, render_template, jsonify, Response
from random import randint
from datetime import date

import requests
import copy
import mysql.connector
import json

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    return render_template('home.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        uname = request.form['uname']
        psw = request.form['psw']
        payload = {'uname':uname, 'psw':psw}
        r = requests.post('http://server:4001/login', json=payload)
        return render_template('login.html', value=r.text)
    return render_template('login.html')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form['username']
        last = request.form['last']
        first = request.form['first']
        address = request.form['address']
        number = request.form['number']
        email = request.form['email']
        psw = request.form['psw']
        pswrepeat = request.form['psw-repeat']
        payload = {'username':username, 'last':last, 'first':first, 'address':address, 'number':number, 'email':email, 'psw':psw, 'psw-repeat':pswrepeat}
        r = requests.post('http://server:4001/register', json=payload)
        return render_template('register.html', value=r.text[0], correct = r.text[1])
    return render_template('register.html')

@app.route('/make_transaction', methods = ['POST', 'GET'])
def make_transaction():
    return render_template('make_transaction.html')

@app.route('/transaction_history', methods = ['POST', 'GET'])
def transaction_history():
    return render_template('transaction_history.html')

@app.route('/show_cards', methods = ['POST', 'GET'])
def show_cards():
    return render_template('show_cards.html')

@app.route('/change_pin', methods = ['POST', 'GET'])
def change_pin():
    return render_template('change_pin.html')

@app.route('/create_card', methods = ['POST', 'GET'])
def create_card():
    return render_template('create_card.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5005')
