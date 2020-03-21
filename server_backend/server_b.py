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


server_b = Flask(__name__)

@server_b.route('/', methods = ['POST', 'GET'])
def home():
    return "Home"

@server_b.route('/login', methods = ['POST', 'GET'])
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

if __name__ == '__main__':
    server_b.debug = True
    server_b.run(host='0.0.0.0', port='4001')
