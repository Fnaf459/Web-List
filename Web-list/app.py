from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# URL для получения данных о расписании
API_BASE_URL = 'https://vm.nathoro.ru/timetable/by-group/'

@app.route('/', methods=['GET', 'POST'])
def timetable():
    group = request.form.get('group', 'ПИбд-42')
    error_message = None
    timetable_data = []

    if request.method == 'POST' and 'clear' in request.form:
        return render_template('timetable.html', timetable=[], group='')

    if request.method == 'POST':
        try:
            response = requests.get(API_BASE_URL + group)
            response.raise_for_status()
            timetable_data = response.json()
        except requests.exceptions.HTTPError as http_err:
            error_message = f'HTTP ошибка: {http_err.response.status_code} {http_err.response.reason}'
        except requests.exceptions.RequestException as req_err:
            error_message = f'Ошибка при запросе: {req_err}'
        except ValueError:
            error_message = 'Ошибка обработки данных от сервера.'

    return render_template('timetable.html', timetable=timetable_data, group=group, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
