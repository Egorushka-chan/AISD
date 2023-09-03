import random
from tkinter import *
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
        for i in range(1, self.K + 1):
            cost = random.randint(COST_MIN, COST_MAX)
            film_array.append(Film(i, cost))

        program_list, max, min = self.create_program_array(film_array.copy(), self.N)

        showing_list = program_list

        str_max, str_min = '', ''

        total_max = 0
        for film in max:
            total_max += film.cost
        str_max = f'Самая дорогая программа - |{[str(film.id) + " " for film in max]}| ценой {total_max}'
        total_min = 0
        for film in min:
            total_min += film.cost
        str_min = f'Самая дешевая программа - |{[str(film.id) + " " for film in min]}| ценой {total_min}'

        return showing_list, str_max, str_min


class OutputForm():
    def __init__(self, result, input_form):
        self.root = Tk()
        self.root.title('Окно вывода')

        self.max_label = Label(self.root, text=result[1]).grid(row=0, column=0)
        self.min_label = Label(self.root, text=result[2]).grid(row=1, column=0)

        results_str = []
        for program in result[0]:
            strng = ''
            for film in program:
                strng += f'{film.id} '
            results_str.append(strng)

        self.listbox = Listbox(self.root, width=20, height=50)

        for i in results_str:
            self.listbox.insert(0, i)

        self.listbox.grid(row=2, column=0)
        input_form.destroy()
        self.root.mainloop()


class InputForm():
    def __init__(self):
        self.root = Tk()
        self.root.title('Окно ввода')

        self.K = 0
        self.stage = 0
        self.N = 0

        Label(self.root, text='Введите значение:').grid(row=0, column=0)
        self.input_entry = Entry(self.root)
        self.input_entry.grid(row=1, column=0)

        Button(self.root, command=self.process, text='Обработать').grid(row=2, column=0)
        self.info_label = Label(self.root,
                                text='Введите число K, которое определяет количество доступных фильмов на хостинге (K > 0) = ',
                                fg='black')
        self.info_label.grid(row=3, column=0, padx=10, pady=10)

        self.root.mainloop()

    def process(self):
        if self.stage == 0:
            K = int(self.input_entry.get())
            if K <= 0:
                self.info_label['text'] = 'Пожалуйста, заново введите КОРРЕКТНОЕ число K (K > 0)'
                self.info_label['foreground'] = 'red'
            else:
                self.stage += 1
                self.info_label['text'] = 'Теперь введите число N, которое определяет кочичество фильмов в программе (N ≤ K) = '
                self.info_label['foreground'] = 'black'
                self.K = K
        elif self.stage == 1:
            N = int(self.input_entry.get())
            if N >= self.K:
                self.info_label['text'] = 'Пожалуйста, заново введите КОРРЕКТНОЕ число N (N ≤ K)'
                self.info_label['foreground'] = 'red'
            else:
                self.N = N
                hosting = Hosting(self.K, self.N)
                result = hosting.make_program_set()
                OutputForm(result, self.root)



if __name__ == "__main__":
    try:
        InputForm()
    except ValueError:
        print(f"ValueError - вы неправильно ввели данные.")
    except Exception as e:
        print(f'Внимание! Неизв. ошибка: {e}')
