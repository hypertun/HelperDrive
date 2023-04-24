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

from datetime import datetime
from pydoc import Helper
from flask import Flask, render_template, request, flash, url_for
from flaskext.mysql import MySQL
from classes import helpers
from classes.helpers import Helper
import os

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'webadmin'
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get(
    'MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = 'helper_drive'
app.config['MYSQL_DATABASE_HOST'] = '116.86.63.183'
app.config['SECRET_KEY'] = os.urandom(24)
mysql.init_app(app)


@app.route("/")
def index():
    conn = mysql.connect()
    data = helpers.getAllHelpers(conn)
    conn.close()
    return render_template('helpers.html', listOfHelpers=data, pages=generate_page_list())


@app.route("/addEditHelper", defaults={'id': None}, methods=["GET", "POST"])
@app.route("/addEditHelper/<id>", methods=["GET", "POST"])
def addEditHelper(id):
    if request.method == "GET":
        if id is None:
            return render_template("addEditHelper.html", pages=generate_page_list(), helper=None)
        else:
            conn = mysql.connect()
            helper = Helper("", "", "", "", "", "")
            helper.id = id
            fullDetails = helper.get(conn)
            conn.close()
            return render_template("addEditHelper.html", pages=generate_page_list(), helper=fullDetails)
    elif request.method == "POST":
        conn = mysql.connect()
        name, code, status, nationality, medical, staffId, err = validationForAdd(
            request)
        id, dob, arrivalDate, flightNo, fin = validationForUpdate(request)
        if not err:
            if id == "NA":
                helper = addEditHelper(conn, None, name, code, status, nationality, medical,
                                       staffId, dob, arrivalDate, flightNo, fin)
            else:
                helper = addEditHelper(conn, id, name, code, status, nationality, medical,
                                       staffId, dob, arrivalDate, flightNo, fin)
                conn.close()
                return render_template("addEditHelper.html", pages=generate_page_list(), helper=helper)
        conn.close()
        return render_template("addEditHelper.html", pages=generate_page_list(), helper=None)
        


@app.route("/delHelper", methods=["GET", "POST"])
def delHelper():
    if request.method == "GET":
        return render_template("delHelper.html", pages=generate_page_list())
    elif request.method == "POST":
        conn = mysql.connect()
        id = request.form["id"]
        delHelper(conn, id)
        conn.close()
        return render_template("delHelper.html", pages=generate_page_list())


def create_app():
    return app


def addEditHelper(conn, id, name, code, status, nationality, medical, staffId, dob, arrivalDate, flightNo, fin):
    newHelper = Helper(name=name, code=code, status=status,
                       nationality=nationality, medical=medical, staff_Id=staffId)
    newHelper.date_of_birth = dob
    newHelper.arrival_date = arrivalDate
    newHelper.flight_no = flightNo
    newHelper.fin = fin
    if id is None:
        newHelper.add(conn)
        flash('New Helper Added!','info')
    else:
        newHelper.id = id
        newHelper.edit(conn)
        flash('Helper Edited!','info')
    return newHelper


def delHelper(conn, id):
    newHelper = Helper(name="", code="", status="",
                       nationality="", medical="", staff_Id=1)
    newHelper.id = id
    newHelper.delete(conn)


def validationForAdd(request):
    error = False
    name = request.form["name"]
    if not name:
        flash('Name is required!','error')
        error = True
    code = request.form["code"]
    if not code:
        flash('Code is required!','error')
        error = True
    status = request.form["status"].casefold()
    if not status or (status != "fresh" and status != "transfer"):
        flash('Status is required as fresh/transfer!','error')
        error = True
    nationality = request.form["nationality"].casefold()
    if not nationality or (nationality != "indonesia" and nationality != "myanmar" and nationality != "philippines"):
        flash('Nationality is required as Indonesia/Myanmar/Philippines!','error')
        error = True
    medical = request.form["medical"].casefold()
    if not medical or (medical != "pass" and medical != "fail"):
        flash('Medical is required as pass/fail!','error')
        error = True
    staffId = request.form["staff_Id"]
    if not code:
        flash('StaffId is required!','error')
        error = True

    return name, code, status, nationality, medical, staffId, error


def validationForUpdate(request):
    id = request.form["id"]
    dob = request.form["dob"]
    if dob != "":
        dob = datetime.strptime(dob, '%Y-%m-%d')
    arrivalDate = request.form["arrivalDate"]
    if arrivalDate != "":
        arrivalDate = datetime.strptime(arrivalDate, '%Y-%m-%dT%H:%M')
    flightNo = request.form["flightNo"]
    fin = request.form["fin"]

    return id, dob, arrivalDate, flightNo, fin


def generate_page_list():
    pages = [
        {"name": "HelperList", "url": url_for("index")},
        {"name": "Add", "url": url_for("addEditHelper")},
        {"name": "Del", "url": url_for("delHelper")},
    ]
    return pages
