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
from flask import Flask, render_template, request, flash,url_for
from flaskext.mysql import MySQL
from classes.helpers import Helper
import os

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'webadmin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'helper_drive'
app.config['MYSQL_DATABASE_HOST'] = '116.86.63.183'
app.config['SECRET_KEY'] = os.urandom(24)
mysql.init_app(app)


@app.route("/")
def index():
    conn = mysql.connect()
    data = getAllHelpers(conn)
    conn.close()
    return render_template('helpers.html', listOfHelpers=data,pages=generate_page_list())


@app.route("/addHelper", methods=["GET", "POST"])
def addHelper():
    if request.method == "GET":
        return render_template("addHelper.html",pages=generate_page_list())
    elif request.method == "POST":
        conn = mysql.connect()
        name,code,status,nationality,medical,staffId,err = validationForAdd(request)
        if not err:
            addHelper(conn, name, code, status, nationality, medical, staffId)
        conn.close()
        return render_template("addHelper.html",pages=generate_page_list())


@app.route("/delHelper", methods=["GET", "POST"])
def delHelper():
    if request.method == "GET":
        return render_template("delHelper.html",pages=generate_page_list())
    elif request.method == "POST":
        conn = mysql.connect()
        id = request.form["id"]
        print(id)
        delHelper(conn, id)
        conn.close()
        return render_template("delHelper.html",pages=generate_page_list())


def create_app():
    return app


def getAllHelpers(conn):
    cursor = conn.cursor()

    helperList = []
    cursor.execute("SELECT * from helpers")
    data = cursor.fetchall()

    for eachHelper in data:
        id, name, code, dob, arrival_Date, flight_No, status, nationality, fin, medical, staff_id, created_at, updated_at = eachHelper
        newHelper = Helper(name,
                           code,
                           status,
                           nationality,
                           medical,
                           staff_id,
                           )
        newHelper.id = id
        newHelper.dob = dob
        newHelper.arrivalDate = arrival_Date
        newHelper.flightNo = flight_No
        newHelper.fin = fin
        newHelper.createdAt = created_at
        newHelper.updatedAt = updated_at

        helperList.append(newHelper)

    cursor.close()
    return helperList


def addHelper(conn, name, code, status, nationality, medical, staffId):
    newHelper = Helper(name=name, code=code, status=status,
                       nationality=nationality, medical=medical, staff_Id=staffId)
    newHelper.add(conn)


def delHelper(conn, id):
    newHelper = Helper(name="May Fen Tei", code="Aw 1276", status="fresh",
                       nationality="Myanmar", medical="pass", staff_Id=1)
    newHelper.id = id
    newHelper.delete(conn)


def validationForAdd(request):
    error = False
    name = request.form["name"]
    code = request.form["code"]
    status = request.form["status"].casefold()
    if not status or (status != "fresh" and status != "transfer"):
        flash('Status is required as fresh/transfer!')
        error=True
    nationality = request.form["nationality"].casefold()
    if not nationality or (nationality != "indonesia" and nationality != "myanmar" and nationality != "philippines"):
        flash('Nationality is required as Indonesia/Myanmar/Philippines!')
        error=True
    medical = request.form["medical"].casefold()
    if not medical or (medical != "pass" and medical != "fail"):
        flash('Medical is required as pass/fail!')
        error=True
    staffId = request.form["staff_Id"]
    return name,code,status,nationality,medical,staffId,error

def generate_page_list():
    pages = [
        {"name": "HelperList", "url": url_for("index")},
        {"name": "Add", "url": url_for("addHelper")},
        {"name": "Del", "url": url_for("delHelper")}, 
    ]
    return pages