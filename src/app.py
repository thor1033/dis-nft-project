from flask import Flask, render_template, redirect, url_for
import pandas as pd

app = Flask(__name__ , static_url_path='/static')

data = pd.read_csv("attributes.csv", dtype=str)

print(list(data[data.id == '0009'].values)[0])

@app.route("/")
def home():
    return render_template("index.html")

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
    app.run()
