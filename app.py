from flask import Flask, render_template, redirect, url_for, session, request, flash
import os

app = Flask(__name__)
app.secret_key = "bugwise_secret_key"  # change later for security

# ---------- ROUTES ---------- #
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ---------- MAIN ---------- #
if __name__ == "__main__":
    app.run(debug=True)
