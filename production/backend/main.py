"""
Copyright @emontj 2024
"""

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from production.backend.collector import update_data
from production.backend.source_configs import PRODUCTION_NEWS_SOURCES

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.sqlite3'

@app.route("/")
def main():
    return '''
     <form action="/echo_user_input" method="POST">
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text

@app.route('/update_data', methods=['GET'])
def update_and_save():
    update_data(PRODUCTION_NEWS_SOURCES, db.engine)

db = SQLAlchemy(app)
class Users(db.Model):
    id = db.Column("User_ID", db.Integer, primary_key=True)
    name = db.Column(db.String(20))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
