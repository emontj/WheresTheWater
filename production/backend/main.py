"""
Copyright @emontj 2024
"""

import time

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pandas as pd

from production.backend.collector import update_data
from production.backend.analyzer import run_analysis
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
def analyze_data():
    try:
        analysis_df = run_analysis(db.engine, limit = 5)
        print(analysis_df)

        return 'analyzed'
    except Exception as e:
        return str(e)

@app.route('/topic/<string:topic_name>', methods=['GET'])
def get_topic_by_name(topic_name):
    query = text('SELECT * FROM analyzed_rss WHERE topic = :topic_name')

    with db.engine.connect() as connection:
        result = connection.execute(query, {'topic_name': topic_name})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    if df.empty:
        return jsonify({'error': 'No records with search term'}), 404
    else:
        topic_dict = df.to_dict(orient='records')
        return jsonify(topic_dict)

@app.route('/person/<string:person_name>', methods=['GET'])
def get_person_by_name(person_name):
    query = text('SELECT * FROM analyzed_rss WHERE individuals LIKE :person_name')

    with db.engine.connect() as connection:
        result = connection.execute(query, {'person_name': f'%{person_name}%'})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    if df.empty:
        return jsonify({'error': 'No records with search term'}), 404
    else:
        topic_dict = df.to_dict(orient='records')
        return jsonify(topic_dict)

@app.route('/posting/<string:hashed_title>', methods=['GET'])
def get_posting_by_id(hashed_title):
    query = text('''
        SELECT * FROM news_rss
        JOIN analyzed_rss ON news_rss.hashed_title = analyzed_rss.hashed_title
        WHERE news_rss.hashed_title = :hashed_title
    ''')

    with db.engine.connect() as connection:
        result = connection.execute(query, {'hashed_title': hashed_title})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    if df.empty:
        return jsonify({'error': 'No records with search term'}), 404
    else:
        topic_dict = df.to_dict(orient='records')
        return jsonify(topic_dict)

@app.route('/raw_posting/<string:hashed_title>', methods=['GET'])
def get_raw_posting_by_id(hashed_title):
    query = text('SELECT * FROM news_rss WHERE hashed_title = :hashed_title')

    with db.engine.connect() as connection:
        result = connection.execute(query, {'hashed_title': hashed_title})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    if df.empty:
        return jsonify({'error': 'No records with search term'}), 404
    else:
        topic_dict = df.to_dict(orient='records')
        return jsonify(topic_dict)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
