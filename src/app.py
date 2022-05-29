from flask import Flask, render_template, redirect, url_for
import pandas as pd

app = Flask(__name__ , static_url_path='/static')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/punk/<punkid>")
def punkpage(punkid):

    """
    Instead of PunkID we would have our database content
    for 1 cryptopunk instead.
    """

    return render_template("cryptopunk.html", content=punkid)

if __name__ == "__main__":
    app.run()
