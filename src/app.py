import random
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import sqlite3

# configuration
DATABASE = '/tmp/flaskr.db'

app = Flask(__name__)
app.config.from_object(__name__)


def get_excuse():
    cur = g.db.execute('select title from excuses order by random() limit 1')
    return cur.fetchone()[0]


@app.route("/")
def index():
    return render_template("message.html", excuse=get_excuse())

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)
