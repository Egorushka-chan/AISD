import csv
import os

import tkinter.messagebox
from tkinter import *

BOARD_VERTICAL_HEADERS = {
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "E",
    6: "F",
    7: "G",
    8: "H"
}

BOARD_PLAYER_TYPE = {
    True: 'X',
    False: 'O'
}


class Board(Frame):
    def __init__(self, master, width, height, x_max, y_max,coloring,  movement_method = None, *args, **kwargs):
        super().__init__(master=master, width=width, height=height, *args, **kwargs)
        self.movement_method = movement_method

        desk_bg_color = '#6C3600'
        desk_fg_color = "#FFFFFF"
        self.x_max = x_max  # height & кол-во вертикалей (А-Н)
        self.y_max = y_max  # width & кол-во горизонталей (1-8)

        headers_size = 20
        button_size_width = (self["width"] - headers_size) // self.y_max
        button_size_height = (self['height'] - headers_size) // self.x_max

        horizontal_header_element_size = (self['height'] - headers_size) // self.x_max
        horizontal_headers_frame = Frame(self, bg=desk_bg_color, width=headers_size,
                                         height=self['height'] - headers_size)
        horizontal_headers_frame.grid(row=0, column=0)
        for i in range(1, self.x_max + 1):
            start_x = 0
            start_y = (horizontal_header_element_size - 1) * (i - 1)
            Label(horizontal_headers_frame, text=str(i), bg=desk_bg_color, fg=desk_fg_color).place(
                x=start_x,
                y=start_y,
                width=headers_size,
                height=horizontal_header_element_size
            )

        vertical_header_element_size = (self["width"] - headers_size) // self.y_max
        vertical_headers_frame = Frame(self, bg=desk_bg_color, height=headers_size, width=self["width"] - headers_size)
        vertical_headers_frame.grid(row=1, column=1)
        for i in range(1, self.y_max + 1):
            start_y = 0
            start_x = (vertical_header_element_size - 1) * (i - 1)
            Label(vertical_headers_frame, text=f"{BOARD_VERTICAL_HEADERS[i]}", bg=desk_bg_color,
                  fg=desk_fg_color).place(
                x=start_x,
                y=start_y,
                width=vertical_header_element_size,
                height=headers_size
            )

        corner_headers_frame = Frame(self, bg=desk_bg_color, height=headers_size, width=headers_size)
        corner_headers_frame.grid(row=1, column=0)

        self.button_list = []
        buttons_canvas = Canvas(self, height=self['height'] - headers_size - 4, width=self["width"] - headers_size - 5)
        buttons_canvas.grid(row=0, column=1)
        for x in range(1, self.x_max + 1):
            start_height = 0 + (button_size_height * (x - 1))
            for y in range(1, self.y_max + 1):
                start_width = 0 + (button_size_width * (y - 1))
                button = Button(buttons_canvas, font=('Inter', 16 * -1),
                                command=lambda _x=x, _y=y: self.press(_x, _y))
                if coloring:
                    if (x+y) % 2 == 0:
                        button.configure(background='black')
                    else:
                        button.configure(background='white')
                button.place(
                    x=start_width,
                    y=start_height,
                    width=button_size_width,
                    height=button_size_height
                )
                self.button_list.append((x, y, button))

    def press(self, x, y):
        if self.movement_method is not None:
            self.movement_method(x, y)

    def place(self, x, y, value):
        for button_cortege in self.button_list:
            if (button_cortege[0] == x) and (button_cortege[1] == y):
                button = button_cortege[2]
                button['text'] = value

class MainForm:
    def __init__(self, path, controller, user):
        self.path = path
        window = Tk()
        window.title('Шашки')

        window.geometry("1280x720")
        window.configure(bg="#FFFFFF")

        canvas = Canvas(
            window,
            bg="#FFFFFF",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        canvas.create_rectangle(
            0.0,
            0.0,
            230.0,
            720.0,
            fill="#E3E3E3",
            outline="")

        try:
            button_image_1 = PhotoImage(
                master=window,
                file=self.relative_to_assets("button_1.png"))
        except:
            button_1 = Button(
                window,
                text='Играть',
                bg='grey',
                borderwidth=0,
                highlightthickness=0,
                command=lambda: print("button_1 clicked"),
                relief="flat"
            )
        else:
            button_1 = Button(
                window,
                image=button_image_1,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: print("button_1 clicked"),
                relief="flat"
            )

        button_1.place(
            x=0.0,
            y=0.0,
            width=219.0,
            height=62.0
        )

        canvas.create_rectangle(
            8.0,
            562.0,
            219.0,
            563.0,
            fill="#000000",
            outline="")

        canvas.create_text(
            17.0,
            577.0,
            anchor="nw",
            text="Пользователь:",
            fill="#000000",
            font=("Inter", 16 * -1)
        )

        canvas.create_text(
            29.0,
            615.0,
            anchor="nw",
            text=user.name,
            fill="#000000",
            font=("Inter", 16 * -1)
        )

        canvas.create_text(
            17.0,
            650.0,
            anchor="nw",
            text="Побед:",
            fill="#000000",
            font=("Inter", 16 * -1)
        )

        canvas.create_text(
            29.0,
            675.0,
            anchor="nw",
            text=user.victories,
            fill="#000000",
            font=("Inter", 16 * -1)
        )

        self.board_frame = Frame(canvas, bg="#FFFFFF", borderwidth=1, relief=SOLID)
        self.board_frame.place(
            x=500,
            y=100,
            width=500,
            height=500
        )

        self.board = None
        self.board = Board(self.board_frame,
                           width=500,
                           height=500,
                           x_max=8,
                           y_max=8,
                           coloring=True)
        self.board.pack()

        self.controller = controller
        self.controller.loginForm.close()
        window.resizable(False, False)
        window.mainloop()

    def relative_to_assets(self, path: str):
        return self.path + r'/mainForm/' + path


class LoginForm:
    def __init__(self, path, controller):
        self.path = path
        self.window = Tk()
        self.window.title('Приветствуем! Войдите в программу')

        self.window.geometry("700x500")
        self.window.configure(bg="#FFFFFF")

        canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=500,
            width=700,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)

        try:
            image_image_1 = PhotoImage(
                file=self.relative_to_assets("image_1.png"))
            image_1 = canvas.create_image(
                190.00000000000006,
                207.0,
                image=image_image_1
            )
        except:
            pass

        canvas.create_rectangle(
            380.99999999999994,
            0.0,
            700.0,
            414.0,
            fill="#D9D9D9",
            outline="")

        canvas.create_rectangle(
            5.684341886080802e-14,
            414.0,
            700.0,
            500.0,
            fill="#124432",
            outline="")

        canvas.create_text(
            406.99999999999994,
            192.0,
            anchor="nw",
            text="Пароль",
            fill="#000000",
            font=("Inter", 24 * -1)
        )
        try:
            entry_image_1 = PhotoImage(
                file=self.relative_to_assets("entry_1.png"))
            entry_bg_1 = canvas.create_image(
                540.0,
                249.5,
                image=entry_image_1
            )
        except:
            pass
        password_entry = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        password_entry.place(
            x=414.99999999999994,
            y=229.0,
            width=250.0,
            height=39.0
        )

        canvas.create_rectangle(
            404.99999999999994,
            280.0,
            675.0,
            281.0,
            fill="#000000",
            outline="")

        canvas.create_text(
            406.99999999999994,
            46.0,
            anchor="nw",
            text="Логин",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        try:
            entry_image_2 = PhotoImage(
                file=self.relative_to_assets("entry_2.png"))
            entry_bg_2 = canvas.create_image(
                540.0,
                106.5,
                image=entry_image_2
            )
        except:
            pass
        login_entry = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        login_entry.place(
            x=414.99999999999994,
            y=86.0,
            width=250.0,
            height=39.0
        )

        canvas.create_rectangle(
            404.99999999999994,
            138.0,
            675.0,
            139.0,
            fill="#000000",
            outline="")

        canvas.create_text(
            26.999999999999943,
            437.0,
            anchor="nw",
            text="Шашки - Компьютерная логическая игра",
            fill="#FFFFFF",
            font=("Inter", 32 * -1)
        )

        try:
            login_button_image = PhotoImage(
                file=self.relative_to_assets("button_1.png"))
        except:
            login_button = Button(
                text='ВХОД',
                bg='Green',
                fg='white',
                borderwidth=0,
                highlightthickness=0,
                activebackground="#D9D9D9",
                command=lambda: controller.send_login(login_entry.get().strip(), password_entry.get().strip()),
                relief="flat"
            )
        else:
            login_button = Button(
                image=login_button_image,
                borderwidth=0,
                highlightthickness=0,
                activebackground="#D9D9D9",
                command=lambda: controller.send_login(login_entry.get().strip(), password_entry.get().strip()),
                relief="flat"
            )
        login_button.place(
            x=397.99999999999994,
            y=336.0,
            width=134.0,
            height=44.0
        )

        try:
            registation_button_image = PhotoImage(
                file=self.relative_to_assets("button_2.png"))
        except:
            registration_button = Button(
                text='Регистрация',
                bg='red',
                fg='white',
                borderwidth=0,
                highlightthickness=0,
                activebackground="#D9D9D9",
                command=lambda: controller.open_registration(),
                relief="flat"
            )
        else:
            registration_button = Button(
                image=registation_button_image,
                borderwidth=0,
                highlightthickness=0,
                activebackground="#D9D9D9",
                command=lambda: controller.open_registration(),
                relief="flat"
            )

        registration_button.place(
            x=547.0,
            y=337.0,
            width=134.0,
            height=44.0
        )

        self.controller = controller
        self.controller.loginForm = self

        self.window.resizable(False, False)
        self.window.mainloop()

    def relative_to_assets(self, path: str):
        return self.path + r'/loginForm/' + path

    def show_error(self, message):
        tkinter.messagebox.showerror(master=self.window, message=message, title='Ошибка')

    def close(self):
        self.window.destroy()


class RegistrationForm:
    def __init__(self, path, controller):
        self.path = path
        self.window = Tk()
        self.window.title('Регистрация')

        self.window.geometry("331x500")
        self.window.configure(bg="#ffffff")

        canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=500,
            width=331,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        canvas.create_rectangle(
            21.0,
            24.0,
            310.0,
            398.0,
            fill="#ECECEC",
            outline="")

        try:
            button_image_1 = PhotoImage(
                master=self.window,
                file=self.relative_to_assets("button_1.png"))
        except:
            button_1 = Button(
                self.window,
                text='Регистрация',
                fg='white',
                bg='red',
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.controller.send_registration(login_entry.get().strip(),
                                                                  password_entry.get().strip(),
                                                                  name_entry.get().strip()),
                relief="flat"
            )
        else:
            button_1 = Button(
                self.window,
                image=button_image_1,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.controller.send_registration(login_entry.get().strip(),
                                                                  password_entry.get().strip(),
                                                                  name_entry.get().strip()),
                relief="flat"
            )
        button_1.place(
            x=28.0,
            y=430.0,
            width=276.0,
            height=44.0
        )

        canvas.create_text(
            45.0,
            43.0,
            anchor="nw",
            text="Логин",
            fill="#000000",
            font=("Inter", 16 * -1)
        )

        try:
            entry_image_1 = PhotoImage(
                master=self.window,
                file=self.relative_to_assets("entry_1.png"))
            entry_bg_1 = canvas.create_image(
                166.0,
                92.0,
                image=entry_image_1
            )
        except:
            pass
        login_entry = Entry(
            self.window,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        login_entry.place(
            x=54.0,
            y=74.0,
            width=224.0,
            height=34.0
        )

        try:
            entry_image_2 = PhotoImage(
                master=self.window,
                file=self.relative_to_assets("entry_2.png"))
            entry_bg_2 = canvas.create_image(
                166.0,
                209.0,
                image=entry_image_2
            )
        except:
            pass

        password_entry = Entry(
            self.window,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        password_entry.place(
            x=54.0,
            y=191.0,
            width=224.0,
            height=34.0
        )

        canvas.create_text(
            45.0,
            160.0,
            anchor="nw",
            text="Пароль",
            fill="#000000",
            font=("Inter", 16 * -1)
        )

        try:
            entry_image_3 = PhotoImage(
                master=self.window,
                file=self.relative_to_assets("entry_1.png"))
            entry_bg_3 = canvas.create_image(
                167.0,
                326.0,
                image=entry_image_3
            )
        except:
            pass
        name_entry = Entry(
            self.window,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        name_entry.place(
            x=55.0,
            y=308.0,
            width=224.0,
            height=34.0
        )

        canvas.create_text(
            46.0,
            277.0,
            anchor="nw",
            text="Имя пользователя",
            fill="#000000",
            font=("Inter", 16 * -1)
        )
        self.controller = controller
        self.controller.registrationForm = self

        self.window.resizable(False, False)
        self.window.mainloop()

    def relative_to_assets(self, path: str):
        return self.path + r'/registrationForm/' + path

    def show_error(self, message):
        tkinter.messagebox.showerror(master=self.window, message=message, title='Ошибка')

    def close(self):
        self.window.destroy()


class User:
    def __init__(self, login, name, victories):
        self.login = login
        self.name = name
        self.victories = victories


class Controller:
    def __init__(self):
        self.assets_path = os.path.dirname(os.path.realpath(__file__)) + r"\assets"
        self.loginForm = None
        self.mainForm = None
        self.registrationForm = None
        self.current_user = None

    def open_login(self):
        self.loginForm = LoginForm(self.assets_path, self)

    def open_registration(self):
        self.registrationForm = RegistrationForm(self.assets_path, self)

    def open_main(self):
        self.mainForm = MainForm(self.assets_path, self, self.current_user)

    def send_registration(self, login, password, name):
        result = self.create_user(login, password, name)
        if result == True:
            self.registrationForm.close()
        else:
            self.registrationForm.show_error('result')

    def send_login(self, login, password):
        user = self.find_user(login, password)
        if user:
            self.current_user = User(user[2], user[3], user[4])
            self.open_main()
        else:
            self.loginForm.show_error('Пользователь не найден')

    def find_user(self, login, password=None):
        with open('users.csv', 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                if password is None:
                    if row[1].strip() == login:
                        return row
                elif (row[1].strip() == login) and (row[2].strip() == password):
                    return row
            return False

    def create_user(self, login, password, name):
        try:
            if self.find_user(login):
                return 'Пользователь с таким логином уже существует'
            with open('users.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(
                    (
                        4,
                        login,
                        password,
                        name,
                        0
                    )
                )
        except Exception as ex:
            return 'Ошибка работы с файлом: ' + str(ex)
        return True


if __name__ == '__main__':
    controller = Controller()
    controller.open_login()
