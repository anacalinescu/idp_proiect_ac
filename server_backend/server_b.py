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


server = Flask(__name__)

@server.route('/', methods = ['POST', 'GET'])
def home():
    return "Home"

@server.route('/login', methods = ['POST', 'GET'])
def login():
    payload = request.get_json(silent=True)
    if not payload:
        return Response(status=400)
    else:
        connection = mysql.connector.connect(**config)
        mycursor = connection.cursor()
        func = "SELECT findUser(%s, %s)"
        mycursor.execute(func, (payload['uname'], payload['psw']))
        val = mycursor.fetchone()
        result = val[0]
        connection.commit()
        connection.close()
        return result

@server.route('/register', methods = ['POST', 'GET'])
def register():
    payload = request.get_json(silent=True)
    if not payload:
        return Response(status=400)
    else:
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
        return "00"

if __name__ == '__main__':
    server.debug = True
    server.run(host='0.0.0.0', port='4001')
