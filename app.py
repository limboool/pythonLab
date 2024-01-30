from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    a = float(request.form['a'])
    b = float(request.form['b'])
    hypotenuse = (a**2 + b**2)**0.5
    area = 0.5 * a * b
    return render_template('result.html', hypotenuse=hypotenuse, area=area)

@app.route('/calculate_sum_or_difference', methods=['POST'])
def calculate_sum_or_difference():
    a = float(request.form['a'])
    b = float(request.form['b'])

    if a > b:
        c = float(request.form['c'])
        sum_result = a + b + c
        result_message = f"Сумма всех трех чисел: {sum_result}"
    elif a == b:
        result_message = "Равны"
    else:
        c = float(request.form['c'])
        difference = a - b - c
        result_message = f"Разность a - b - c: {difference}\nЗадание завершено"

    return render_template('result_lab2.html', result=result_message)

@app.route('/replace_character', methods=['POST'])
def replace_character():
    input_string = request.form['input_string']
    key = request.form['key']

    # Заменяем символы в строке
    result_string = input_string.replace(key, "NULL")

    return render_template('result_lab3.html', result=result_string)

@app.route('/insert_into_array', methods=['POST'])
def insert_into_array():
    array_C = [1, 2, 3, 2, 1, 10, 15, 122, 12]
    number = int(request.form['number'])
    position = int(request.form['position'])

    # Добавляем число в массив на указанную позицию
    array_C.insert(position, number)

    return render_template('result_lab4.html', result=array_C)

@app.route('/capitalize_word', methods=['POST'])
def capitalize_word():
    input_word = request.form['input_word']

    # Проверяем, что слово не пустое
    if not input_word:
        result_message = "Пустая строка"
    else:
        # Возвращаем слово с измененной первой буквой
        result_message = input_word[0].upper() + input_word[1:]

    return render_template('result_lab5.html', result=result_message)

# Скрипт для работы с датой
def read_date_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            date_str = file.read().strip()
            return datetime.strptime(date_str, '%Y-%m-%d')
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return None
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return None

def write_date_to_file(file_path, date):
    try:
        with open(file_path, 'w') as file:
            file.write(date.strftime('%Y-%m-%d'))
    except Exception as e:
        print(f"Произошла ошибка при записи в файл: {e}")

def get_next_day(current_date):
    return current_date + timedelta(days=1)

@app.route('/next_day', methods=['POST'])
def next_day():
    file_path = 'date_file.txt'

    current_date = read_date_from_file(file_path)

    if current_date:
        next_day_date = get_next_day(current_date)
        write_date_to_file(file_path, next_day_date)

        return render_template('result_lab6.html', current_date=current_date.strftime('%Y-%m-%d'),
                               next_day=next_day_date.strftime('%Y-%m-%d'), result="Дата успешно записана в файл.")
    else:
        return render_template('result_lab6.html', current_date="Не удалось получить текущую дату из файла.",
                               next_day="", result="")

if __name__ == '__main__':
    app.run(debug=True)
