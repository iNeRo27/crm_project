from flask import Flask, render_template, request, redirect
from models import db, User, Request
from flask import session   
from datetime import datetime

app = Flask(__name__)

#  Secret key
app.config['SECRET_KEY'] = 'secret123'

#  Database config (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# connect db with app
db.init_app(app)

# home route
@app.route("/")
def home():
    return "CRM is running "

# register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        # create new user
        new_user = User(name=name, password=password)

        db.session.add(new_user)
        db.session.commit()

        return redirect("/")

    return render_template("register.html")

# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        # check user in database
        user = User.query.filter_by(name=name, password=password).first()

        if user:
            # save session
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["role"] = user.role

            # redirect based on role
            if user.role == "admin":
                return redirect("/admin")
            else:
                return redirect("/request")
        else:
            return "Invalid name or password"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    return f"Welcome {session['user_name']} "

# request route
@app.route("/request", methods=["GET", "POST"])
def request_page():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        req_type = request.form["type"]
        description = request.form["description"]
        phone = request.form["phone"]

        new_request = Request(
            user_id=session["user_id"],
            type=req_type,
            description=description,
            phone=phone,
            created_at=datetime.now()
        )

        db.session.add(new_request)
        db.session.commit()

        return "Request submitted successfully ✅ <a href='/request'>Submit another</a>"

    return render_template("request.html")

# admin route
@app.route("/admin")
def admin_dashboard():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect("/login")

    requests = Request.query.all()

    return render_template("admin_dashboard.html", requests=requests)

# Logout route
@app.route("/logout")
def logout():
    session.clear()  # remove all session data
    return redirect("/login")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create tables

        # create admin 
        if not User.query.filter_by(name="admin").first():
            admin = User(name="admin", password="admin123", role="admin")
            db.session.add(admin)
            db.session.commit()

            
    app.run(debug=True)