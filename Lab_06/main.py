# Задание состоит из двух частей.
# 1 часть – написать программу в соответствии со своим вариантом задания.
# 2 часть – усложнить написанную программу, введя по своему усмотрению в условие минимум одно
# ограничение на характеристики объектов и целевую функцию для оптимизации решения.

# Вариант 1
# Видео-хостинг подготовил к просмотру К фильмов. По абонементу можно выбрать любую
# программу, состоящую из N фильмов. Сформировать все возможные варианты программ.

# Придуманое мною усложнение:
# В каждой программе должно быть минимум 1, при K = 1, или 2, при K > 1, патриотических фильма
# Каждая программа должна быть уникальна (не должно существовать программы с одинаковыи фильмами)

import random


class Film:
    def __init__(self, id, is_patriotic=False):
        self.id = id
        self.is_patriotic = is_patriotic


def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)


def placement(n, k):
    return factorial(n) / factorial(n - k)


def first_part(K, N):
    def create_program_array(film_array, depth, program_array, input_program):  # первая часть
        if depth == 0:
            program_array.append(input_program)
        else:
            for film in film_array:
                if depth > 0:
                    if film not in input_program:
                        self_program = input_program.copy()
                        self_program.append(film)
                        create_program_array(film_array, depth - 1, program_array, self_program)
        return program_array

    print('---------------------ЧАСТЬ 1. Базовая программа---------------------------------')

    film_array = [Film(i) for i in range(1, K + 1)]  # создаем набор фильмов

    print('\nСозданы фильмы:')
    for film in film_array[:5]:
        print(f'{film.id}')
    if K > 5:
        print('etc.')

    program_list = create_program_array(film_array, N, [], [])

    print('\nСозданы программы:')
    for program in program_list[:30]:
        str = ''
        for film in program:
            str += f'{film.id} '
        print(str)
    if len(program_list) > 30:
        print('etc.')
    print(f'\nКоличество различных программ = {len(program_list)}')
    print(f'\nМатематическое размещение показывает, что правильный ответ должен быть ', placement(K, N))


def second_part(K, N):
    def create_program_array(film_array, depth, program_array, input_program):  # первая часть
        if depth == 0:
            program_array.append(input_program)
        else:
            for film in film_array:
                if len(input_program) == 0:
                    film_array.remove(film)
                if depth > 0:
                    if film not in input_program:
                        if (film.is_patriotic) or (len([i for film in input_program if film.is_patriotic]) >= 2):
                            self_program = input_program.copy()
                            self_program.append(film)
                            create_program_array(film_array, depth - 1, program_array, self_program)
        return program_array
    print('---------------------ЧАСТЬ 2. Усложнённая программа---------------------------------')

    patriotic_chance = 1
    film_array = []
    patriotic_count = 0
    for i in range(1, K + 1):
        chance = random.random()
        if chance <= patriotic_chance:
            is_patriotic = True
            patriotic_count += 1
            if patriotic_count >= 2:
                patriotic_chance = 0.2
        else:
            is_patriotic = False
        film_array.append(Film(i, is_patriotic))

    print('\nСозданы фильмы:')
    for film in film_array[:10]:
        str = ''
        if film.is_patriotic:
            str = ', патриотический'
        print(f'{film.id}{str}')
    if K > 10:
        print('etc.')
    print('\nКол-во патриотического кино:', patriotic_count)

    program_list = create_program_array(film_array.copy(), N, [], [])

    print('\nСозданы программы:')
    for program in program_list[:30]:
        str = ''
        for film in program:
            str += f'{film.id} '
        print(str)
    if len(program_list) > 30:
        print('etc.')
    print(f'\nКоличество уникальных программ = {len(program_list)}')


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
