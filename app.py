from flask import Flask, render_template, request, redirect
from models import db, User
from flask import session   

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

        user = User.query.filter_by(name=name, password=password).first()

        if user:
            session["user_id"] = user.id
            session["user_name"] = user.name

            return redirect("/dashboard")
        else:
            return "Invalid name or password"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    return f"Welcome {session['user_name']} "

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create tables
    app.run(debug=True)