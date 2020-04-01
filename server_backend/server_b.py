from typing import List, Dict
from flask import Flask
from flask import request, render_template, jsonify, Response
from random import randint
from datetime import date

import requests
import copy
import mysql.connector
import json

config = {
'user': 'ana',
'password': 'idp',
'host': 'db',
'port': '3306',
'database': 'idp_banking'
}

accountno = 0


server = Flask(__name__)

@server.route('/logout', methods = ['POST', 'GET'])
def logout():
    global accountno
    payload = request.get_json(silent=True)
    if not payload:
        return Response(status=400)
    else:
        accountno = 0

@server.route('/', methods = ['POST', 'GET'])
def home():
    return "Home"

@server.route('/login', methods = ['POST', 'GET'])
def login():
    global accountno
    payload = request.get_json(silent=True)
    if not payload:
        return Response(status=400)
    else:
        connection = mysql.connector.connect(**config)
        mycursor = connection.cursor()
        func = "SELECT findUser(%s, %s)"
        mycursor.execute(func, (payload['uname'], payload['psw']))
        val = mycursor.fetchone()
        result = str(val[0])
        connection.commit()
        func = "SELECT getAccountNo(%s, %s)"
        mycursor.execute(func, (payload['uname'], payload['psw']))
        acc = mycursor.fetchone()
        accountno = acc[0]
        connection.commit()
        connection.close()
        return result

@server.route('/register', methods = ['POST', 'GET'])
def register():
    global accountno
    payload = request.get_json(silent=True)
    if not payload:
        return Response(status=400)
    else:
        if accountno != 0:
            connection = mysql.connector.connect(**config)
            if payload['psw'] == payload['psw-repeat']:
                mycursor = connection.cursor()
                func = "SELECT correctUsername(%s)"
                mycursor.execute(func, (payload['username'],))
                correct = mycursor.fetchone()
                if correct[0] == 0:
                    mycursor.callproc('insertPersonalData', [payload['username'], payload['last'], payload['first'], payload['address'], payload['number'], payload['email'], ])
                    connection.commit()
                    accountno = randint(10000, 99999)
                    mycursor.callproc('insertUser', [payload['username'], payload['psw'], str(accountno), ])
                    connection.commit()
                connection.close()
                val = "1" + str(correct[0])
                return val
            connection.close()
            return "10"
        return "00"

@server.route('/create_card', methods = ['POST', 'GET'])
def create_card():
    global accountno
    payload = request.get_json(silent=True)
    if not payload:
        return Response(status=400)
    else:
        if accountno != 0:
            connection = mysql.connector.connect(**config)
            mycursor = connection.cursor()
            pin = str(randint(1000, 9999))
            iban = "ANABNK" + str(randint(1000000, 9999999))
            mycursor.callproc('insertCard', [iban, pin, accountno, payload['coin'], ])
            connection.commit()
            connection.close()
            result = str(pin) + " " + str(iban) + " " + "0"
            return result
        result = "pin" + " " + "iban" + " " + "1"
        return result

@server.route('/change_pin', methods = ['POST', 'GET'])
def change_pin():
    global accountno
    payload = request.get_json(silent=True)
    if not payload:
        return Response(status=400)
    else:
        if accountno != 0:
            val = 0
            connection = mysql.connector.connect(**config)
            mycursor = connection.cursor()
            func = "SELECT correctTransfer(%s, %s, %s)"
            mycursor.execute(func, (payload['iban'], accountno ,payload['pin']))
            correct = mycursor.fetchone()
            if correct[0] == 1:
                if payload['new_pin'] == payload['rep_pin']:
                    mycursor = connection.cursor()
                    mycursor.callproc('changePin', [payload['iban'].replace(" ", ""), payload['pin'], payload['new_pin'], ])
                    connection.commit()
                    val = 1
                connection.close()
                result = str(val) + " " + str(0) + " " + str(correct[0])
                return result
            connection.close()
            result = str(val) + " " + str(0) + " " + str(correct[0])
            return result
        result = "-" + " " + str(1) + " " + "-"
        return result

@server.route('/show_cards', methods = ['POST', 'GET'])
def show_cards():
    global accountno
    payload = request.get_json(silent=True)
    if not payload:
        return Response(status=400)
    else:
        if accountno != 0:
            connection = mysql.connector.connect(**config)
            value = []
            mycursor = connection.cursor()
            mycursor.callproc('displayCards', [str(accountno), ])
            connection.commit()
            for result in mycursor.stored_results():
                value = result.fetchall()
            connection.close()
            result = {'flights':value, 'signup':0}
            return result
        result = {'flights': '-', 'signup':1}
        return result

@server.route('/add_money', methods = ['POST', 'GET'])
def add_money():
    global accountno
    payload = request.get_json(silent=True)
    if not payload:
        return Response(status=400)
    else:
        if accountno != 0:
            connection = mysql.connector.connect(**config)
            mycursor = connection.cursor()
            func = "SELECT correctIban(%s, %s)"
            mycursor.execute(func, (payload['iban'].replace(" ", ""), accountno))
            correct = mycursor.fetchone()
            if correct[0] == 1:
                mycursor = connection.cursor()
                mycursor.callproc('addMoney', [payload['iban'].replace(" ", ""), str(accountno), payload['sum'], ])
                connection.commit()
            result = str(0) + " " + str(correct[0])
            return result
        result = str(1) + " " + "-"
        return result

@server.route('/make_transaction', methods = ['POST', 'GET'])
def make_transaction():
    global accountno
    payload = request.get_json(silent=True)
    if not payload:
        return Response(status=400)
    else:
        if accountno != 0:
            connection = mysql.connector.connect(**config)
            mycursor = connection.cursor()
            func = "SELECT correctTransfer(%s, %s, %s)"
            mycursor.execute(func, (payload['source'].replace(" ", ""), accountno ,payload['pin']))
            correct = mycursor.fetchone()
            func = "SELECT enoughMoney(%s, %s, %s, %s)"
            mycursor.execute(func, (payload['source'].replace(" ", ""), accountno ,payload['pin'], payload['sum']))
            enough_money = mycursor.fetchone()
            if correct[0] == 1 and enough_money[0] == 1:
                mycursor.callproc('insertTransaction', [payload['source'].replace(" ", ""), payload['destination'], payload['comm'], payload['sum'], date.today(), ])
                connection.commit()
            connection.close()
            result = str(0) + " " + str(correct[0]) + " " + str(enough_money[0])
            return result
        result = str(1) + " " + "-" + " " + "-"
        return result

@server.route('/transaction_history', methods = ['POST', 'GET'])
def transaction_history():
    global accountno
    payload = request.get_json(silent=True)
    if not payload:
        return Response(status=400)
    else:
        if accountno != 0:
            connection = mysql.connector.connect(**config)
            value = []
            mycursor = connection.cursor()
            func = "SELECT correctIban(%s, %s)"
            mycursor.execute(func, (payload['iban'].replace(" ", ""), accountno))
            correct = mycursor.fetchone()
            if correct[0] == 1:
                mycursor.callproc('displayTransactions', [payload['iban'].replace(" ", ""), ])
                connection.commit()
                for result in mycursor.stored_results():
                    value = result.fetchall()
                connection.close()
                result = {'flights':value, 'signup':0, 'correct':correct[0]}
                return result
            connection.close()
            result = {'correct':correct[0], 'signup':0}
            return result
        result = {'correct':"-", 'signup':1}
        return result

if __name__ == '__main__':
    server.debug = True
    server.run(host='0.0.0.0', port='4001')
