"""
Натуральные числа, не превышающие 1 000 000, у которых пятая справа цифра равна 7.
Выводит на экран четные цифры стоящие в числе справа от этой 7 (прописью).
"""
import re

numbers_dictionary = { # для вывода прописью
    '0': 'ноль',
    '2': 'два',
    '4': 'четыре',
    '6': 'шесть',
    '8': 'восемь',
}

general_regex = re.compile('\d?7\d{4}')
even_regex = re.compile('[02468]')
split_regex = re.compile('7\d{4}$')


with open("numbers.txt", 'r') as file:
    file_body = file.read()
    if file_body:
        has_requied_value = False
        file_values = general_regex.findall(file_body)
        for raw_value in file_values:
            splited_value = split_regex.findall(raw_value)
            result = splited_value[0] # берем правую часть

            result_chars = []
            for char in result:
                if even_regex.search(char):
                    result_chars.append(char)

            result_string = ''
            for result_char in result_chars:
                result_string += numbers_dictionary[result_char] + " "
            if result_string != '':
                has_requied_value = True
                print(f"{raw_value}: {result_string}")
        if not has_requied_value:
            print('В файле отсутствуют подходящие значения')
    else:
        print('Файл пустой')


