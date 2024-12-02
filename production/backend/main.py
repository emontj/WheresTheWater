"""
Copyright @emontj 2024
"""

import time

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from production.backend.collector import update_data
from production.backend.analyzer import read_table
from production.backend.source_configs import PRODUCTION_NEWS_SOURCES

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.sqlite3'
last_feed_update = 0
db = SQLAlchemy(app)

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
    global last_feed_update

    now = time.time()
    if now - last_feed_update > 3600:
        update_data(PRODUCTION_NEWS_SOURCES, db.engine)
        analyze_data()
        last_feed_update = now
        return 'Feed updated'
    else:
        return 'Check feed later, updated too frequently'

@app.route('/analyze', methods=['GET'])
def analyze_data(): # TODO
    df = read_table(db.engine, 'news_rss')
    print(df.columns)
    return 'Analyzed'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
