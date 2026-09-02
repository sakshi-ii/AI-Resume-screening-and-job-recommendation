from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "ai_resume_project_secret_key"


# ==============================
# DATABASE CONNECTION
# ==============================

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="S@kshi04012005",
        database="ai_resume_db"
    )


# ==============================
# HOME
# ==============================

@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# REGISTER
# ==============================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO users (name, email, password, role)
                VALUES (%s, %s, %s, %s)
                """,
                (name, email, password, "user")
            )

            conn.commit()

            return "Registration successful! You can now login."

        except mysql.connector.Error as e:
            return "Registration error: " + str(e)

        finally:
            cursor.close()
            conn.close()

    return render_template("register.html")


# ==============================
# LOGIN
# ==============================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and user["password"] == password:

            session["user_id"] = user["id"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return "Admin Login Successful!"

            return redirect(url_for("user_dashboard"))

        return "Invalid email or password!"

    return render_template("login.html")


# ==============================
# USER DASHBOARD
# ==============================

@app.route("/user-dashboard")
def user_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "user":
        return redirect(url_for("login"))

    return render_template("user_dashboard.html")


# ==============================
# LOGOUT
# ==============================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ==============================
# TEST DATABASE
# ==============================

@app.route("/test-db")
def test_db():

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT DATABASE()")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return "Database connected successfully! Database: " + str(result[0])

    except Exception as e:
        return "Database connection error: " + str(e)


# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    app.run(debug=True)

    print("App file started!")
