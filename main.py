from flask import Flask, render_template
import requests

app = Flask(__name__)

res = requests.get("https://api.npoint.io/8a2f0b7cba1b18c6eaea")
res.raise_for_status()

posts = res.json()

@app.route("/")
def index():
    return render_template("index.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)