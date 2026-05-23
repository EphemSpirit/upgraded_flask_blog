from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import smtplib
import os

app = Flask(__name__)
load_dotenv()

res = requests.get("https://api.npoint.io/8a2f0b7cba1b18c6eaea")
res.raise_for_status()

posts = res.json()

@app.route("/")
def index():
    return render_template("index.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html", form_redirect=False)
    else:
        with smtplib.SMTP(os.getenv("SMTP_HOST"), port=587) as connection:
            connection.starttls()
            connection.login(
                user=os.getenv("GMAIL_ADDRESS"),
                password=os.getenv("GMAIL_APP_PASSWORD")
            )
            connection.sendmail(
                from_addr=request.form["email"],
                to_addrs=os.getenv("GMAIL_ADDRESS"),
                msg=f"Subject: Contact from {request.form['name']}\n\n{request.form['message']}"
            )
        return render_template("contact.html", form_redirect=True)


@app.route("/posts/<int:id>")
def post_show(id):
    requested_post = None

    for post in posts:
        if post["id"] == id:
            requested_post = post

    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)