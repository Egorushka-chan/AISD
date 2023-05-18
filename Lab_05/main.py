# Задана рекуррентная функция. Область определения функции – натуральные числа.
# Написать программу сравнительного вычисления данной функции рекурсивно и
# итерационно. Определить границы применимости рекурсивного и итерационного
# подхода. Результаты сравнительного исследования времени вычисления представить в
# табличной и графической форме в виде отчета по лабораторной работе.

#	F(1) = 2; G(1) = 1; F(n) = (n–1)! – G(n–1), G(n) = F(n–1) + G(n–1), при n >=2

import time
from matplotlib import pyplot as plt

F_START = 2
G_START = 1
N_RECURSION_MAX = 36  # число N, более которого выводится предупреждение о слишком большой рекурсии


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

    print('\nВыполнение итерации...')
    start = time.time()
    result_iteration = f_iteration(N)
    end = time.time()
    print(f'\nРезультат работы итерационного подхода - {result_iteration}\nЗатраченное время - {end - start}')

    answer = '1'
    if N >= N_RECURSION_MAX:
        print('\nЧисло n слишком большое для рекурсивного подхода, и может занять многооо времени')
        answer = input('Введите 1, если хотите выполнить расчет, или 0, если нет - ')
        while answer not in ('1', '0'):
            print('Вы ввели не 1 и не 0!')
            answer = int(input('Введите 1, если хотите выполнить расчет, или 0, если нет'))

    if answer == '1':
        print('\nВыполнение рекурсии...')
        start = time.time()
        result_recursion = f_recursion(N)
        end = time.time()
        print(f'\nРезультат работы рекурсивного подхода - {result_iteration}\nЗатраченное время - {end - start}')

    print('\nСделать сравнительную таблицу рекурсивного и итерационного подхода?')
    if (N >= N_RECURSION_MAX):
        print(f'Внимание! Число N больше {N_RECURSION_MAX}, и расчет займет много времени!')
    answer = input('Введите 1, если хотите выполнить расчет, или 0, если нет - ')
    while answer not in ('1', '0'):
        print('Вы ввели не 1 и не 0!')
        answer = int(input('Введите 1, если хотите выполнить расчет, или 0, если нет'))

    if answer == '1':
        recursive_time = []
        iteration_time = []

        for n in range(1, N):
            start = time.time()
            f_recursion(n)
            end = time.time()
            recursive_time.append(end - start)

            start = time.time()
            f_iteration(n)
            end = time.time()
            iteration_time.append(end - start)

        fig, ax = plt.subplots()
        ax.set(title='Сравнение итерационного и рекурсивного подхода', xlabel='N', ylabel='Время, сек.')
        ax.plot(recursive_time, label='Рекурсия')
        ax.plot(iteration_time, label='Итерация')
        ax.set_xticks(range(N))

        plt.show()

    print('Создать график итерационного подхода? Шаг - 1000'
          '\nВведите 0 - не создавать'
          '\nВведите 1 - до 20000, займёт ~3 секунды'
          '\nВведите 2 - до 50000, займёт ~40 секунд'
          '\nВведите 3 - до 200000, займёт ~10 минут')
    answer = input('Ответ = ')
    while answer not in ('1', '0', '2', '3'):
        print('Вы ввели неверное значение')
        answer = int(input('Введите 0, 1, 2, 3 ='))
    if answer in ('1', '2', '3'):
        MAX = 21000
        if answer == '2':
            MAX = 51000
        if answer == '3':
            MAX = 210000

        iteration_range = range(1000, MAX, 1000)
        iteration_time = []

        for i in iteration_range:
            start = time.time()
            f_iteration(i)
            end = time.time()
            iteration_time.append(end - start)

        fig, ax = plt.subplots()
        ax.set(title='График итерационного подхода', xlabel='N', ylabel='Время, сек.')
        ax.plot(iteration_range,iteration_time, label = 'Итерация')

        plt.show()

except ValueError:
    print(f"ValueError - вы неправильно ввели данные.")
except Exception as e:
    print(f'Внимание! Неизв. ошибка: {e}')
