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

admin = Flask(__name__)

def space_generator(n):
    res = ""
    for i in range(1, n + 1):
        res = res + " "
    return res

@admin.route('/', methods = ['POST', 'GET'])
def home():
    if request.method == "POST":
        command = request.form['command']
        connection = mysql.connector.connect(**config)
        mycursor = connection.cursor(buffered=True)
        mycursor.execute(command)
        connection.commit()
        responses = mycursor.fetchall()
        connection.close()
        response = []
        for elements in responses:
            resp = ""
            for element in elements:
                resp = resp + str(element) + space_generator(30 - len(str(element)))
            response.append(resp)

        return render_template('admin.html', response = response)
    return render_template('admin.html', response = "")

if __name__ == '__main__':
    admin.debug = True
    admin.run(host='0.0.0.0', port='5004')