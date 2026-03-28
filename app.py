from flask import Flask
from models import db

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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create tables
    app.run(debug=True)