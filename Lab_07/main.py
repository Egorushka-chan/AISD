import random
from collections import deque


class Film:
    def __init__(self, id, cost=0):
        self.id = id
        self.cost = cost


class Hosting:
    def sum(self, program):
        sum = 0
        for film in program:
            sum += film.cost
        return sum

    def create_program_array(self, film_array, depth):
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

        max = program_array[0]
        min = program_array[0]
        for program in program_array:
            if self.sum(program) > self.sum(max):
                max = program
            if self.sum(program) < self.sum(min):
                min = program

        return program_array, max, min

    def __init__(self, K, N):
        self.K = K
        self.N = N

    def make_program_set(self):
        film_array = []
        COST_MAX = 1500
        COST_MIN = 200
        for i in range(1, K + 1):
            cost = random.randint(COST_MIN, COST_MAX)
            film_array.append(Film(i, cost))

        print('\nСозданы фильмы:')
        for film in film_array:
            print(f'{film.id}, {film.cost} руб.')

        program_list, max, min = self.create_program_array(film_array.copy(), N)

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

        hosting = Hosting(K, N)
        hosting.make_program_set()
    except ValueError:
        print(f"ValueError - вы неправильно ввели данные.")
    except Exception as e:
        print(f'Внимание! Неизв. ошибка: {e}')
