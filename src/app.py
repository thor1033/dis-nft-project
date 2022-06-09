from flask import Flask, render_template, redirect, url_for, session, abort, request, flash
import os
import pandas as pd
import random

app = Flask(__name__ , static_url_path='/static')

data = pd.read_csv("attributes.csv", dtype=str)


@app.route("/", methods=["POST", "GET"])
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == "POST":
            input_gender = request.form["radio"]
            input_type = request.form["radiotype"]
            input_skin = request.form["radioskin"]

            input_count = request.form["accessCount"] or 0
            input_access = request.form["access"] or "NaN"

            return redirect(url_for("querypage", gender=input_gender, types=input_type, skin=input_skin, access=input_access, count=input_count))
            
        punks = data.values[:10]
        length = len(punks)
        randomNumber = random.choice([id[0] for id in data.values])
        return render_template("index.html", content=punks, length=length, randomNumber = randomNumber)

@app.route("/punks/<gender>/<types>/<skin>/<count>/<access>")
def querypage(gender, types, skin, count, access):
    ct = data.copy()
    if gender != "Both":
        ct = ct[ct["gender"] == gender]

    if types != "All":
        ct = ct[ct["type"] == types]

    if skin != "All":
        ct = ct[ct["skin tone"] == skin]

    if access != "NaN":
        ct = ct[ct["accessories"].str.contains(access)]
    print(ct)
    if count != 0:
        ct = ct[ct["count"] == count]

    ct = list(ct.values)[1:]
    length = len(ct)
    return render_template("cryptoquery.html", content=ct, length=length)


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/punk/<punkid>")
def punkpage(punkid):

    """
    Instead of PunkID we would have our database content
    for 1 cryptopunk instead.
    """

    print(punkid)
    ct = list(data[data.id == punkid].values)[0]
    return render_template("cryptopunk.html", content=ct)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()
