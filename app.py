#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#
#  Copyright 2022 ivan <hypertun@ivan-hpnotebook>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from pydoc import Helper
from flask import Flask, render_template
from flaskext.mysql import MySQL
from classes.helper import Helper

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'webadmin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'helper_drive'
app.config['MYSQL_DATABASE_HOST'] = '116.86.63.183'
mysql.init_app(app)


@app.route("/")
def index():
    data = getAllHelpers()
    return render_template('addnewmaid.html', listOfHelpers=data)


def create_app():
    return app


def getAllHelpers():
    conn = mysql.connect()
    cursor = conn.cursor()

    helperList = []
    cursor.execute("SELECT * from helpers")
    data = cursor.fetchall()

    for eachHelper in data:
        id, name, code, dob, arrival_Date, status, nationality = eachHelper
        newHelper = Helper(id, name, dob, code,
                           arrival_Date, status, nationality)
        helperList.append(newHelper)

    return helperList
