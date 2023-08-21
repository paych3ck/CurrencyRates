import csv
import datetime
import requests
import xml.etree.ElementTree as ET


def valutes_parser():
    url_date = datetime.date.today().strftime('%d-%m-%Y')
    url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={url_date}"

    response = requests.get(url)

    if response.status_code != 200:
        return 'Ошибка!'

    xml_data = response.text
    root = ET.fromstring(xml_data)
    csv_file = 'valutes.csv'

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['CharCode', 'Name'])

        for valute in root.iter('Valute'):
            char_code = valute.find('CharCode').text
            name = valute.find('Name').text
            writer.writerow([char_code, name])


valutes_parser()
