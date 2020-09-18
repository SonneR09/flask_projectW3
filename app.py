import json
from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms import validators


class BookingForm(FlaskForm):
    name = StringField('Имя', [validators.InputRequired(message="Введите имя.")])
    phone = StringField('Телефон', [validators.InputRequired(message='Введите номер.')])
    clientWeekday = HiddenField('clientWeekday')
    clientTime = HiddenField('clientTime')
    clientTeacher = HiddenField('clientTeacher')


app = Flask(__name__)
app.secret_key = ('pgPhsrZR4DqDWHxV')

with open('database\\teachers_data.json', 'r') as f:
    teachers_data = json.loads(f.read())

with open('database\\goals_data.json', 'r') as f:
    goals_data = json.loads(f.read())


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/goals/<goal>/')
def goals(goal):
    return render_template('goal.html')


@app.route('/profiles/<int:id>/')
def profile(id):
    return render_template('profile.html', teachers=teachers_data, goals=goals_data, id=id)


@app.route('/request/')
def request():
    return render_template('request.html')


@app.route('/request_done/')
def request_done():
    return render_template('request_done.html')


@app.route('/booking/<int:id>/<week>/<time>/')
def booking(id, week, time):
    booking_form = BookingForm()
    return render_template('booking.html', form=booking_form, id=id, week=week, time=time,
                           teachers=teachers_data, goals=goals_data)


@app.route('/booking_done/', methods=["GET", "POST"])
def booking_done():
    booking_form = BookingForm()
    name = booking_form.name.data
    phone = booking_form.phone.data
    weekDay = booking_form.clientWeekday.data
    time = booking_form.clientTime.data
    teach_id = int(booking_form.clientTeacher.data)

    if booking_form.validate_on_submit():
        info = {'Имя': name, 'Телефон': phone, 'День недели': weekDay, 'Время': time,
                'Учитель': teachers_data[teach_id]['name']}

        with open('database\\clientBase.json', 'r') as f:
            list_of_clients = json.loads(f.read())
        list_of_clients.append(info)
        with open('database\\clientBase.json', 'w') as f:
            f.write(json.dumps(list_of_clients))

        return render_template('booking_done.html', name=name, phone=phone, weekDay=weekDay, time=time,
                               teachers=teachers_data, id=teach_id)
    return redirect(f'/booking/{str(teach_id)}/{weekDay}/{time}')


if __name__ == '__main__':
    app.run(debug=True)
