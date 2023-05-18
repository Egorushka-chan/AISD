# Задание состоит из двух частей.
# 1 часть – написать программу в соответствии со своим вариантом задания.
# 2 часть – усложнить написанную программу, введя по своему усмотрению в условие минимум одно
# ограничение на характеристики объектов и целевую функцию для оптимизации решения.

# Вариант 1
# Видео-хостинг подготовил к просмотру К фильмов. По абонементу можно выбрать любую
# программу, состоящую из N фильмов. Сформировать все возможные варианты программ.

# Придуманое мною усложнение:
# У каждой программы должна быть цена
# Нужно высчитать самую дешевую и дорогую программу


import random
from collections import deque


class Film:
    def __init__(self, id, cost=0):
        self.id = id
        self.cost = cost


def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def placement(n, k):
    return factorial(n) / factorial(n - k)


def first_part(K, N):
    def create_program_array(film_array, depth):
        production = deque()
        result_program_array = []
        for film in film_array:
            production.append([film])

        while len(production):
            program = production.popleft()
            for film in film_array:
                if film not in program:
                    self_program = program.copy()
                    self_program.append(film)

                    if len(self_program) == depth:
                        result_program_array.append(self_program)
                    else:
                        production.append(self_program)

        return result_program_array

    print('---------------------ЧАСТЬ 1. Базовая программа---------------------------------')

    film_array = [Film(i) for i in range(1, K + 1)]  # создаем набор фильмов

    print('\nСозданы фильмы:')
    [print(f'{film.id}') for film in film_array]

    program_list = create_program_array(film_array, N)

    print(f'\nКоличество различных программ = {len(program_list)}')
    print(f'\nМатематическое размещение показывает, что правильный ответ должен быть ', placement(K, N))

    showing_list = program_list
    if len(program_list) > 30:
        quantity = int(input(f'Введите 0 - чтобы вывести все.'
                             f'\nВведите другое число - чтобы вывести кол-во программ, равное этому числу.'
                             f'\nОтвет = '))
        if quantity != 0:
            showing_list = program_list[:quantity]
    for program in showing_list:
        str = ''
        for film in program:
            str += f'{film.id} '
        print(str)


def second_part(K, N):
    def create_program_array(film_array, depth):
        production = deque()
        program_array = []
        for film in film_array:
            production.append([film])

        while len(production):
            program = production.popleft()
            for film in film_array:
                if film not in program:
                    self_program = program.copy()
                    self_program.append(film)

                    if len(self_program) == depth:
                        program_array.append(self_program)
                    else:
                        production.append(self_program)

        def sum(program):
            sum = 0
            for film in program:
                sum += film.cost
            return sum

        max = program_array[0]
        min = program_array[0]
        for program in program_array:
            if sum(program) > sum(max):
                max = program
            if sum(program) < sum(min):
                min = program

        return program_array, max, min



    print('---------------------ЧАСТЬ 2. Усложнённая программа---------------------------------')

    film_array = []
    COST_MAX = 1500
    COST_MIN = 200
    for i in range(1, K + 1):
        cost = random.randint(COST_MIN, COST_MAX)
        film_array.append(Film(i, cost))

    print('\nСозданы фильмы:')
    for film in film_array:
        print(f'{film.id}, {film.cost} руб.')

    program_list, max, min = create_program_array(film_array.copy(), N)

    print(f'\nКоличество различных программ = {len(program_list)}')

    showing_list = program_list
    if len(program_list) > 30:
        quantity = int(input(f'Введите 0 - чтобы вывести все.'
                             f'\nВведите другое число - чтобы вывести кол-во программ, равное этому числу.'
                             f'\nОтвет = '))
        if quantity != 0:
            showing_list = program_list[:quantity]
    for program in showing_list:
        strng = ''
        for film in program:
            strng += f'{film.id} '
        print(strng)

    total_max = 0
    for film in max:
        total_max += film.cost
    print(f'Самая дорогая программа - |{[str(film.id) + " " for film in max]}| ценой {total_max}')
    total_min = 0
    for film in min:
        total_min += film.cost
    print(f'Самая дешевая программа - |{[str(film.id) + " " for film in min]}| ценой {total_min}')




if __name__ == "__main__":
    try:
        K = int(input('Введите число K, которое определяет количество доступных фильмов на хостинге (K > 0) = '))
        while K <= 0:
            print('Пожалуйста, заново введите КОРРЕКТНОЕ число K')
            K = int(input('Введите число K, которое определяет количество доступных фильмов на хостинге (K > 0) = '))
        N = int(input('Введите число N, которое определяет кочичество фильмов в программе (N ≤ K) = '))
        while N >= K:
            print('Пожалуйста, заново введите КОРРЕКТНОЕ число N')
            N = int(input('Введите число N, которое определяет кочичество фильмов в программе (N ≤ K) = '))
        first_part(K, N)
        input('\nВведите что-угодно для продолжения...')
        second_part(K, N)
    except ValueError:
        print(f"ValueError - вы неправильно ввели данные.")
    except Exception as e:
       print(f'Внимание! Неизв. ошибка: {e}')
