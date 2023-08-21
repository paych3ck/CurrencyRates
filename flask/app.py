from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField
from wtforms.validators import DataRequired

import csv
import secrets
import requests
import datetime
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

csv_file = 'valutes.csv'
choices = []

with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        choices.append((row[0], row[1]))


class CurrencyForm(FlaskForm):
    code = SelectField('Выберите валюту', choices=choices)
    date = DateField('Дата', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Получить курс')


def get_currency_rate(code, date):
    input_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    url_date = input_date.strftime('%d-%m-%Y')
    url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={url_date}'

    response = requests.get(url)

    xml_data = response.text
    root = ET.fromstring(xml_data)
    valute_element = root.find(f'.//Valute[CharCode="{code.upper()}"]')

    value_element = valute_element.find('Value')
    value = value_element.text

    name_element = valute_element.find('Name')
    name = name_element.text

    return f'{code} ({name}): {value}'


@app.route('/', methods=['GET', 'POST'])
def currency_rate():
    form = CurrencyForm()
    if form.validate_on_submit():
        code = form.code.data
        date = form.date.data.strftime('%Y-%m-%d')
        result = get_currency_rate(code, date)
        return render_template('index.html', form=form, result=result)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run()
