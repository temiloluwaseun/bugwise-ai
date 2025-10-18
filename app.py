# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection, init_db
import os

app = Flask(__name__)
app.secret_key = "bugwise_secret_key"

# Initialize DB
init_db()

# ---------- ROUTES ---------- #
@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not username or not email or not password:
            flash("All fields are required!", "error")
            return redirect(url_for("register"))

        from werkzeug.security import generate_password_hash
        conn = get_db_connection()
        cursor = conn.cursor()

        # Hash the password before saving
        hashed_password = generate_password_hash(password)

        # Insert new user into the database
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        conn.commit()
        conn.close()

        flash("Registration successful! You can now login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user"] = user["username"]
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))
    
    username = session["user"]

    # Placeholder stats (later can come from database)
    stats = {
        "reported": 5,
        "in_progress": 2,
        "resolved": 8,
        "projects": 3
    }

    return render_template("dashboard.html", user=username, stats=stats)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
