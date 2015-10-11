import random
from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def index():
    return random.choice(open("resources/excuses.txt").readlines())

if __name__ == '__main__':
    app.run()