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
    payload = {'clicked':1}
    r = requests.post('http://server:4001/logout', json=payload)
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
    if request.method == "POST":
        source = request.form['source']
        destination = request.form['destination']
        pin = request.form['pin']
        comm = request.form['comm']
        ssum = request.form['sum']
        payload = {'source':source, 'destination':destination, 'pin':pin, 'comm':comm, 'sum':ssum}
        r = requests.post('http://server:4001/make_transaction', json=payload)
        return render_template('make_transaction.html', signup=r.text.split(" ")[0], correct=r.text.split(" ")[1], enough_money=r.text.split(" ")[2])
    return render_template('make_transaction.html')

@app.route('/transaction_history', methods = ['POST', 'GET'])
def transaction_history():
    if request.method == "POST":
        iban = request.form['iban']
        payload = {'iban':iban}
        r = requests.post('http://server:4001/transaction_history', json=payload).json()
        if r['correct'] == 1:
            return render_template('transaction_history.html', flights=r['flights'], signup=r['signup'])
        return render_template('transaction_history.html', signup=r['signup'], correct=r['correct'])
    return render_template('transaction_history.html')

@app.route('/show_cards', methods = ['POST', 'GET'])
def show_cards():
    if request.method == "POST":
        key = 'iban'
        if key not in request.form:
            payload = {'clicked':1}
            r = requests.post('http://server:4001/show_cards', json=payload).json()
            return render_template('show_cards.html', flights=r['flights'], signup=r['signup'])
        else:
            iban = request.form['iban']
            ssum = request.form['sum']
            payload = {'iban':iban, 'sum':ssum}
            r = requests.post('http://server:4001/add_money', json=payload)
            return render_template('show_cards.html', signup=r.text.split(" ")[0], correct=r.text.split(" ")[1])
    return render_template('show_cards.html')

@app.route('/change_pin', methods = ['POST', 'GET'])
def change_pin():
    if request.method == "POST":
        iban = request.form['iban']
        pin = request.form['pin']
        new_pin = request.form['new_pin']
        rep_pin = request.form['rep_pin']
        payload = {'iban':iban, 'pin':pin, 'new_pin':new_pin, 'rep_pin':rep_pin}
        r = requests.post('http://server:4001/change_pin', json=payload)     
        return render_template('change_pin.html', value=r.text.split(" ")[0], signup=r.text.split(" ")[1], corrct=r.text.split(" ")[2])   
    return render_template('change_pin.html')

@app.route('/create_card', methods = ['POST', 'GET'])
def create_card():
    if request.method == "POST":
        coin = request.form['coin']
        payload = {'coin':coin}
        r = requests.post('http://server:4001/create_card', json=payload)     
        return render_template('create_card.html', pin=r.text.split(" ")[0], iban=r.text.split(" ")[1], signup=r.text.split(" ")[2])   
    return render_template('create_card.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='4005')
