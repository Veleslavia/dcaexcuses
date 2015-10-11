import random
from flask import Flask, render_template


app = Flask(__name__)
app.config.from_object(__name__)


def get_excuse():
    return unicode(random.choice(open("resources/excuses.txt").readlines()), "utf8")


@app.route("/")
def index():
    return render_template("message.html", excuse=get_excuse())


if __name__ == '__main__':
    app.run(debug=True)