# Задана рекуррентная функция. Область определения функции – натуральные числа.
# Написать программу сравнительного вычисления данной функции рекурсивно и
# итерационно. Определить границы применимости рекурсивного и итерационного
# подхода. Результаты сравнительного исследования времени вычисления представить в
# табличной и графической форме в виде отчета по лабораторной работе.

#	F(1) = 2; G(1) = 1; F(n) = (n–1)! – G(n–1), G(n) = F(n–1) + G(n–1), при n >=2

import time
import datetime
import csv

F_START = 2
G_START = 1


# ---------------------------РЕКУРСИЯ----------------------------
def factorial_recursion(n):
    if n == 1:
        return 1
    else:
        return n * factorial_recursion(n - 1)


def f_recursion(n):
    if n == 1:
        return F_START
    else:
        return factorial_recursion(n - 1) - g_recursion(n - 1)


def g_recursion(n):
    if n == 1:
        return G_START
    else:
        return f_recursion(n - 1) + g_recursion(n - 1)


# ---------------------------ИТЕРАЦИЯ--------------------------------
def factorial_iteration(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def f_iteration(n):
    last_f = F_START
    last_g = G_START
    last_factorial = 1
    for i in range(2, n + 1):
        current_f = last_factorial - last_g
        last_g += last_f
        last_factorial *= i
        last_f = current_f
    return last_f

try:
    N = int(input('Введите число n, являющимся входным для ф-ии, указанной в условии. (n ≥ 2) = '))
    while N < 2:
        print('Число должно быть больше 1-ого. Введите заново!')
        N = int(input('Введите число n, являющимся входным для ф-ии, указанной в условии. (n ≥ 2) = '))

    print('\nАвтотест - анализ времени для выполнения вычисления для всех значений от 2 до n, и запись результатов в файл')
    answer = int(input('Выполнить автотест - 1, просто рассчитать значение для заданного входного значения n - 0\nОтвет: '))
    while answer not in (1, 0):
        print('Вы ввели не 1 и не 0!')
        answer = int(input('Выполнить автотест - 1, просто рассчитать значение для заданного входного значения n - 0\nОтвет: '))

    if answer == 0:
        print('\nВыполнение итерации...')
        start = time.time()
        result_iteration = f_iteration(N)
        end = time.time()
        print(f'\nРезультат работы итерационного подхода - {result_iteration}\nЗатраченное время - {end - start}')

        answer = 1
        if N >= 38:
            print('\nЧисло n слишком большое для рекурсивного подхода, и может занять многооо времени')
            answer = int(input('Введите 1, если хотите выполнить расчет, или 0, если нет - '))
            while answer not in (1, 0):
                print('Вы ввели не 1 и не 0!')
                answer = int(input('Введите 1, если хотите выполнить расчет, или 0, если нет'))

        if answer == 1:
            print('\nВыполнение рекурсии...')
            start = time.time()
            result_recursion = f_recursion(N)
            end = time.time()
            print(f'\nРезультат работы рекурсивного подхода - {result_iteration}\nЗатраченное время - {end - start}')
    else:
        date = f'{datetime.datetime.now().day}.{datetime.datetime.now().month}'
        file_name = f'result_{date}.csv'
        with open(file_name,'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    'n',
                    'Время итерации, сек'
                )
            )
        for n in range(1000, N+1, 1000):
            start = time.time()
            f_iteration(n)
            end = time.time()
            time_iteration = end-start
            with open(file_name, 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(
                    (
                        n,
                        time_iteration
                    )
                )
except ValueError:
    print(f"ValueError - вы неправильно ввели данные.")
except Exception as e:
    print(f'Внимание! Неизв. ошибка: {e}')
