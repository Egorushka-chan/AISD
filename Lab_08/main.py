import os
import random
import tkinter.messagebox
from tkinter import *
from collections import deque

ASSETS_PATH = os.path.dirname(os.path.realpath(__file__)) + r"\assets"


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

        return program_list, max, min


class OutputForm():
    def __init__(self, result, input_form):
        self.window = Tk()
        self.window.title('Вывод')

        self.program_set, self.max_program, self.min_program = result

        self.current_programs = 1
        self.program_range = 12

        self.program_count = len(self.program_set)

        self.window.geometry("873x509")
        self.window.configure(bg="#FFFFFF")

        canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=509,
            width=873,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        canvas.create_rectangle(
            0.0,
            0.0,
            471.0,
            509.0,
            fill="#EDEDED",
            outline="")

        image_image_1 = PhotoImage(
            master=self.window,
            file=self.relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(
            231.0,
            131.0,
            image=image_image_1
        )

        image_image_2 = PhotoImage(
            master=self.window,
            file=self.relative_to_assets("image_2.png"))
        image_2 = canvas.create_image(
            231.0,
            369.0,
            image=image_image_2
        )

        self.poor_frame = Frame(master=canvas, bg='#C8FFD1')
        self.poor_frame.place(
            x=29,
            y=329,
            width=408,
            height=142
        )

        # canvas.create_rectangle( # дешевый
        #     29.0,
        #     329.0,
        #     437.0,
        #     471.0,
        #     fill="#C8FFD1",
        #     outline="")

        image_image_3 = PhotoImage(
            master=self.window,
            file=self.relative_to_assets("image_3.png"))
        image_3 = canvas.create_image(
            51.0,
            285.0,
            image=image_image_3
        )

        self.poor_price_label = Label(master=canvas, bg='#C8FFD1', font=("Inter", 20 * -1))
        self.poor_price_label.place(
            x=185,
            y=291
        )

        canvas.create_text(
            108.0,
            261.0,
            anchor="nw",
            text="Самая дешевая программа",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.rich_frame = Frame(master=canvas, bg='#F6FFBD')
        self.rich_frame.place(
            x=29,
            y=88,
            width=401,
            height=143
        )

        # canvas.create_rectangle( # дорогой
        #     29.0,
        #     88.0,
        #     430.0,
        #     231.0,
        #     fill="#F6FFBD",
        #     outline="")

        image_image_4 = PhotoImage(
            master=self.window,
            file=self.relative_to_assets("image_4.png"))
        image_4 = canvas.create_image(
            51.0,
            47.0,
            image=image_image_4
        )

        self.rich_price_label = Label(master=canvas, bg='#F6FFBD', font=("Inter", 20 * -1))
        self.rich_price_label.place(
            x=185,
            y=58
        )

        canvas.create_text(
            115.0,
            28.0,
            anchor="nw",
            text="Самая дорогая программа",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        canvas.create_rectangle(
            471.0,
            0.0,
            873.0,
            509.0,
            fill="#E3E3E3",
            outline="")

        self.table_frame = Frame(master=canvas, bg="#E4E4E4")
        self.table_frame.place(
            x=493,
            y=70,
            width=350,
            height=400
        )

        rooting = Frame(self.table_frame, bg="#E4E4E4")
        Button(rooting, text='<', command=self.click_back_button).grid(row=0, column=0, pady=2, padx=2)
        Button(rooting, text='>', command=self.click_forward_button).grid(row=0, column=1, pady=2, padx=2)
        self.rooting_label = Label(rooting, bg="#E4E4E4", font=("Inter", 14 * -1), text='1-12')
        self.rooting_label.grid(row=0, column=2, padx=2, pady=2)
        rooting.grid(row=0, column=0)

        self.displayed_programs = []

        self.total_program_label = Label(master=canvas, bg="#E4E4E4", font=("Inter", 20 * -1))
        self.total_program_label.place(
            x=530,
            y=40
        )

        # canvas.create_rectangle( # программы
        #     493.0,
        #     47.0,
        #     843.0,
        #     483.0,
        #     fill="#E4E4E4",
        #     outline="")

        canvas.create_text(
            585.0,
            9.0,
            anchor="nw",
            text="Таблица программ",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        input_form.destroy()
        self.total_program_label['text'] = 'Кол-во различных программ = ' + str(len(self.program_set))
        self.fill_rich_program()
        self.fill_poor_program()
        self.fill_table()

        self.window.resizable(False, False)
        self.window.mainloop()

    def relative_to_assets(self, path: str):
        return ASSETS_PATH + r'/outputForm/' + path

    def fill_rich_program(self):
        self.max_program = sorted(self.max_program, key=lambda film: film.cost, reverse=True)
        total_max = 0
        i = 1
        for film in self.max_program:
            total_max += film.cost

            l = Label(self.rich_frame, font=("Inter", 14 * -1), bg='#F6FFBD')
            l['text'] = f'{i}. ID:{film.id}, Цена:{film.cost}'
            l.pack(anchor=W)
            i += 1
        self.rich_price_label['text'] = str(total_max) + ' рублей'

    def fill_poor_program(self):
        self.min_program = sorted(self.min_program, key=lambda film: film.cost, reverse=True)
        total_min = 0
        i = 1
        for film in self.min_program:
            total_min += film.cost

            l = Label(self.poor_frame, font=("Inter", 14 * -1), bg='#C8FFD1')
            l['text'] = f'{i}. ID:{film.id}, Цена:{film.cost}'
            l.pack(anchor=W)
            i += 1
        self.poor_price_label['text'] = str(total_min) + ' рублей'

    def fill_table(self):
        for p in self.displayed_programs:
            p.destroy()

        for i in range(self.current_programs, self.current_programs+self.program_range):
            if i > self.program_count:
                return
            program = self.program_set[i-1]
            frame = Frame(self.table_frame, bg="#E4E4E4")
            total_price = 0

            Label(frame,font=("Inter", 14 * -1), bg="#E4E4E4", text=f'{i}: ').pack(anchor=W, side=LEFT)

            for film in program:
                l = Label(frame, font=("Inter", 14 * -1), bg="#E4E4E4")
                l['text'] = film.id
                l.pack(anchor=W, pady=2, padx=2, side=LEFT)

                total_price += film.cost

            Label(frame,font=("Inter", 14 * -1), bg="#E4E4E4", text=f'{total_price} руб.').pack(anchor=E, pady=2, padx=2, side=LEFT)
            frame.grid(column=0)
            self.displayed_programs.append(frame)

    def click_back_button(self):
        test = self.current_programs - self.program_range
        if test <= 0:
            return
        self.current_programs = test
        self.rooting_label['text'] = f'{self.current_programs}-{self.program_range+self.current_programs-1}'
        self.fill_table()

    def click_forward_button(self):
        test = self.current_programs + self.program_range
        if test >= self.program_count:
            return
        self.current_programs += self.program_range
        self.rooting_label['text'] = f'{self.current_programs}-{self.program_range+self.current_programs-1}'
        self.fill_table()




class InputForm():
    def __init__(self):
        self.window = Tk()
        self.window.title('Ввод')

        self.window.geometry("768x359")
        self.window.configure(bg="#FFFFFF")

        canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=359,
            width=768,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        canvas.create_rectangle(
            0.0,
            0.0,
            768.0,
            221.0,
            fill="#D9D9D9",
            outline="")

        entry_image_1 = PhotoImage(
            master=self.window,
            file=self.relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            190.5,
            113.5,
            image=entry_image_1
        )
        self.entry_K = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_K.place(
            x=54.0,
            y=96.0,
            width=273.0,
            height=33.0
        )

        entry_image_2 = PhotoImage(
            master=self.window,
            file=self.relative_to_assets("entry_2.png"))
        entry_bg_2 = canvas.create_image(
            596.5,
            113.5,
            image=entry_image_2
        )
        self.entry_N = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_N.place(
            x=460.0,
            y=96.0,
            width=273.0,
            height=33.0
        )

        canvas.create_text(
            44.0,
            64.0,
            anchor="nw",
            text="Кол-во фильмов на хостинге",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        canvas.create_text(
            450.0,
            64.0,
            anchor="nw",
            text="Кол-во фильмов в программе",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        canvas.create_text(
            44.0,
            139.0,
            anchor="nw",
            text="Не больше 7!",
            fill="#000000",
            font=("Inter", 14 * -1)
        )

        canvas.create_text(
            450.0,
            139.0,
            anchor="nw",
            text="Не больше кол-ва на хостинге!",
            fill="#000000",
            font=("Inter", 14 * -1)
        )

        button_enter_image = PhotoImage(
            master=self.window,
            file=self.relative_to_assets("button_1.png"))
        button_enter = Button(
            image=button_enter_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.click_input_button,
            relief="flat"
        )
        button_enter.place(
            x=281.0,
            y=263.0,
            width=207.0,
            height=69.0
        )

        image_image_1 = PhotoImage(
            master=self.window,
            file=self.relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(
            394.0,
            114.0,
            image=image_image_1
        )
        self.window.resizable(False, False)
        self.window.mainloop()

    def relative_to_assets(self, path: str):
        return ASSETS_PATH + r'/inputForm/' + path

    def click_input_button(self):
        K = 0
        N = 0
        try:
            K = int(self.entry_K.get().strip())  # кол-во фильмов на хостинге
            N = int(self.entry_N.get().strip())  # кол-во фильмов в наборе
        except ValueError:
            tkinter.messagebox.showerror('Ошибка валидации', 'Введите натуральное число', master=self.window)
            return

        if K > 7:
            tkinter.messagebox.showerror('Слишком большое число',
                                         'Слишком большое кол-во фильмов на хостинге приведет к очень долгим рассчетам. Снизте количество',
                                         master=self.window)
            return
        if N > K:
            tkinter.messagebox.showerror('Ошибка', 'Фильмов в программе не может быть больше чем на хостинге',
                                         master=self.window)
            return

        hosting = Hosting(K, N)
        result = hosting.make_program_set()

        OutputForm(result, self.window)


if __name__ == "__main__":
    try:
        InputForm()
    except ValueError:
        print(f"ValueError - вы неправильно ввели данные.")
    except Exception as e:
        print(f'Внимание! Неизв. ошибка: {e}')
