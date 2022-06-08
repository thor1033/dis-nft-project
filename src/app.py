from flask import Flask, render_template, redirect, url_for, session, abort, request, flash
import os
import pandas as pd

app = Flask(__name__ , static_url_path='/static')

data = pd.read_csv("attributes.csv", dtype=str)


@app.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template("index.html", content=data.values)

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

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
