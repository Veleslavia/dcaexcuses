# -*- coding: utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, render_template
from contextlib import closing
import sqlite3

# configuration
DATABASE = '/tmp/flaskr.db'
SECRET_KEY = "excuses_key"

app = Flask(__name__)
app.config.from_object(__name__)


class Excuse(object):

    up_text = u"Норм"
    down_text = u"Не катит"

    def __init__(self, id, title, vote_up, vote_down):
        self.id = id
        self.title = title
        self.vote_up = vote_up
        self.vote_down = vote_down

    def do_vote_up(self):
        self.vote_up += 1
        g.db.execute("update excuses set upvotes=upvotes+1 where id = {excuse_id}".format(excuse_id=self.id))
        g.db.commit()
        return self.vote_up

    def do_vote_down(self):
        self.vote_down += 1
        g.db.execute("update excuses set downvotes=downvotes+1 where id = {excuse_id}".format(excuse_id=self.id))
        g.db.commit()
        return self.vote_down

    def update(self):
        cur = g.db.execute('select id, title, upvotes, downvotes from excuses order by random() limit 1')
        self.id, self.title, self.vote_up, self.vote_down = cur.fetchone()


excuse = Excuse(None, None, None, None)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.args.get("up_vote", ""):
        excuse.do_vote_up()
        return render_template("message.html", excuse=excuse)
    if request.args.get("down_vote", ""):
        excuse.do_vote_down()
        return render_template("message.html", excuse=excuse)
    excuse.update()
    return render_template("message.html", excuse=excuse)


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
    app.run()
