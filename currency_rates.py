import argparse
import requests
import datetime
import xml.etree.ElementTree as ET


def get_currency_rate(code, date):
    try:
        input_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    except ValueError:
        print('Введите корректную дату!')
        return

    if input_date > datetime.date.today():
        print('Введите дату до сегодняшнего дня!')
        return

    url_date = input_date.strftime('%d-%m-%Y')
    url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={url_date}'

    response = requests.get(url)

    if response.status_code != 200:
        print('Ошибка при получении курсов валют!')
        return

    xml_data = response.text
    root = ET.fromstring(xml_data)
    valute_element = root.find(f'.//Valute[CharCode="{code.upper()}"]')

    if valute_element is None:
        print(f'Валюта с кодом {code} не найдена')
        return

    value_element = valute_element.find('Value')
    value = value_element.text

    name_element = valute_element.find('Name')
    name = name_element.text

    print(f'{code} ({name}): {value}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Вывод курса валюты ЦБ РФ за определенную дату')
    parser.add_argument('--code', type=str,
                        help='Код валюты в формате ISO 4217')
    parser.add_argument('--date', type=str, help='Дата в формате YYYY-MM-DD')

    args = parser.parse_args()

    if args.code is None or args.date is None:
        parser.print_help()
    else:
        get_currency_rate(args.code, args.date)
