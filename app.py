import json
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length


app = Flask(__name__)
app.secret_key = ('pgPhsrZR4DqDWHxV')


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/goals/<goal>/')
def goals(goal):
    return render_template('goal.html')


@app.route('/profiles/<int:id>/')
def profile(id):

    with open('database\\teachers_data.json', 'r') as f:
        teachers_data = json.loads(f.read())

    with open('database\\goals_data.json', 'r') as f:
        goals_data = json.loads(f.read())


    return render_template('profile.html', teachers=teachers_data, goals=goals_data, id=id)

@app.route('/request/')
def request():
    return render_template('request.html')


@app.route('/request_done/')
def request_done():
    return render_template('request_done.html')


@app.route('/booking/<id>/')
def booking(id):
    return render_template('booking.html')


@app.route('/booking_done/')
def booking_done():
    return render_template('booking_done.html')


if __name__ == '__main__':
    app.run(debug=True)
