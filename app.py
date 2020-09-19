import json
from support import support_scripts, clients
from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, RadioField
from wtforms import validators


class BookingForm(FlaskForm):
    name = StringField('Имя', [validators.InputRequired(message="Введите имя.")])
    phone = StringField('Телефон', [validators.InputRequired(message='Введите номер.')])
    clientWeekday = HiddenField('clientWeekday')
    clientTime = HiddenField('clientTime')
    clientTeacher = HiddenField('clientTeacher')


class RequestForm(FlaskForm):
    goals = RadioField('Какая цель занятий?', choices=[("travel", "Для путешествий"), ("study", "Для учебы"),
                                                       ("work", "Для работы"), ("relocate", "Для переезда")])
    times = RadioField('Какая цель занятий?', choices=[("1", "1-2 часа в неделю"), ("3", "3-5 часов в неделю"),
                                                       ("2", "5-7 часов в неделю"), ("4", "7-10 часов в неделю")])
    name = StringField('Ваше имя', [validators.InputRequired()])
    phone = StringField('Ваш телефон', [validators.InputRequired()])


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
    form = RequestForm()

    return render_template('request.html', form=form)


@app.route('/request_done/',  methods=["GET", "POST"])
def request_done():
    form = RequestForm()
    goal = form.goals.data
    time = form.times.data
    name = form.name.data
    phone = form.name.data
    if form.is_submitted():
        info = {'Имя': name, 'Телефон': phone, 'Цель': goal, 'Время': time}
        clients.add_client_req(info)
        return render_template('request_done.html', goal=goal, time=time, name=name, phone=phone, goals=goals_data)
    return redirect('/request/')


@app.route('/booking/<int:id>/<week>/<time>/')
def booking(id, week, time):
    booking_form = BookingForm()
    path = f'/booking/{str(id)}/{week}/{time}/'

    support_scripts.booking_link_checker(path=path, teachers=teachers_data)  # Проверяет корректность URL
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

    if booking_form.is_submitted():
        info = {'Имя': name, 'Телефон': phone, 'День недели': weekDay, 'Время': time,
                'Учитель': teachers_data[teach_id]['name']}

        clients.add_client(info=info)
        clients.change_status(teach_id, weekDay, time)
        return render_template('booking_done.html', name=name, phone=phone, weekDay=weekDay, time=time,
                               teachers=teachers_data, id=teach_id)
    return redirect(f'/booking/{str(teach_id)}/{weekDay}/{time}')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404', error=error), 404


if __name__ == '__main__':
    app.run(debug=True)
