"""
Натуральные числа, не превышающие 1 000 000, у которых пятая справа цифра равна 7.
Выводит на экран четные цифры стоящие в числе справа от этой 7 (прописью).
"""
numbers_dictionary = {
    '0': 'ноль',
    '1': 'один',
    '2': 'два',
    '3': 'три',
    '4': 'четыре',
    '5': 'пять',
    '6': 'шесть',
    '7': 'семь',
    '8': 'восемь',
    '9': 'девять'
}

dividers_list = {  # разделители слов
    '',
    ' ',
    ','
    '.',
    '   ',
    '\n',
    '-',
    '_',
    ':'
}


def read_block(file):
    symbol = file.read(1)
    result = ''
    while symbol not in dividers_list:
        result += symbol
        symbol = file.read(1)

    if symbol == '':  # проверка на конец файла
        return result, True
    else:
        return result, False


def int_try_parse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


with open("numbers.txt", 'r') as file:
    result = read_block(file)
    number = result[0]
    end_of_file = result[1]

    while end_of_file == False:
        if number:
            test_passed = True
            for value in number:  # проверка что значение содержит только числа
                if value not in numbers_dictionary:
                    test_passed = False

            if test_passed:  # проверка что число не превышает 1 000 000
                parse_result = int_try_parse(number)
                if parse_result[1]:
                    if parse_result[0] > 1000000:
                        test_passed = False

            if test_passed:  # проверка что 5-ое число справа 7
                length = len(number)
                if length >= 5:
                    fifth_value = number[-5]
                    if fifth_value != '7':
                        test_passed = False
                else:
                    test_passed = False

            if test_passed:  # вывод четных чисел
                selected_values = number[-4:]
                result_values = []
                for value in selected_values:
                    if int(value) % 2 == 0:
                        result_values.append(value)

                result_string = ''
                for result_value in result_values:
                    result_string += numbers_dictionary[result_value] + " "
                if result_string != '':
                    print(f"{number}: {result_string}")

        result = read_block(file)
        number = result[0]
        end_of_file = result[1]
    else:
        print('файл пустой')
