from flask import Flask, render_template, redirect, url_for, session, abort, request, flash
import os
import pandas as pd
import random

import requests
from bs4 import BeautifulSoup

app = Flask(__name__ , static_url_path='/static')

data = pd.read_csv("attributes.csv", dtype=str)


@app.route("/", methods=["POST", "GET"])
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == "POST":
            input_gender = request.form["radio"].lower()
            input_type = request.form["radiotype"].lower()
            input_skin = request.form["radioskin"].lower()

            input_count = request.form["accessCount"] or -1
            input_access = request.form["access"].lower() or "NaN"

            input_id = request.form["punkid"].lower() or ""

            if input_id != "":
                input_id = input_id.zfill(4)
                return redirect(url_for("punkpage", punkid=input_id))
            return redirect(url_for("querypage", gender=input_gender, types=input_type, skin=input_skin, access=input_access, count=input_count))
            
        punks = data.values[:10]
        length = len(punks)
        randomNumber = random.choice([id[0] for id in data.values])
        return render_template("index.html", content=punks, length=length, randomNumber = randomNumber)

@app.route("/punks/<gender>/<types>/<skin>/<count>/<access>")
def querypage(gender, types, skin, count, access):
    if not session.get('logged_in'):
        return render_template('login.html')
    ct = data.copy()
    if gender != "both":
        ct = ct[ct["gender"] == gender]

    if types != "all":
        ct = ct[ct["type"] == types]

    if skin != "all":
        ct = ct[ct["skin_tone"] == skin]

    if access != "NaN":
        ct = ct[ct["accessories"].str.contains(access)]

    print(ct)
    if int(count) != -1:
        ct = ct[ct["count"] == count]

    ct = list(ct.values)[1:]
    length = len(ct)
    print(count)
    print(length)
    return render_template("cryptoquery.html", content=ct, length=length)


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return redirect(url_for("home"))

@app.route("/createaccount", methods=['POST', 'GET'])
def createaccount():
    if request.method == 'POST':
        ######GEM ACCOUNT###########
        new_username = request.form['username']
        new_password = request.form['password']
        print("HEJ")
        #######################
        return redirect(url_for("home"))
    return render_template("createaccount.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/profile")
def profile():
    if not session.get('logged_in'):
        return render_template('login.html')
    
    favsid = ['0001', '1234', '8743', '8593']
    favs = list(data[data['id'].isin(favsid)].values)
    length = len(favsid)
    print(favs)
    return render_template("profile.html", content=favs, length=length)


@app.route("/punk/<punkid>", methods=["POST", "GET"])
def punkpage(punkid):

    """
    Instead of PunkID we would have our database content
    for 1 cryptopunk instead.
    """
    if not session.get('logged_in'):
        return render_template('login.html')

    if request.method == "POST":
        # Add til favourite
        print("ADDED TO FAVOURITE")


    req = "https://cryptopunks.app/cryptopunks/details/"+ punkid
    response = requests.get(req)
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.select("table.ms-rteTable-default tr")
    pricelist = str(soup.find(class_="punk-history-row-bid")).split('\n')
    if len(pricelist) < 5:
        price = "10Ξ ($18,000)"
    else:
        price =pricelist[4].replace('</td>', '').replace('<td>','')
    print(punkid)
    print(price)
    ct = list(data[data.id == punkid].values)[0]
    return render_template("cryptopunk.html", content=ct, price=price)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
