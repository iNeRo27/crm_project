from flask import Flask, render_template, request, redirect
from models import db, User

app = Flask(__name__)

#  Secret key
app.config['SECRET_KEY'] = 'secret123'

#  Database config (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# connect db with app
db.init_app(app)

@app.route("/")
def home():
    return "CRM is running "

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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create tables
    app.run(debug=True)