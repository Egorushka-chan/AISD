import tkinter.messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


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
        image_image_1 = PhotoImage(
            file=self.relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(
            190.00000000000006,
            207.0,
            image=image_image_1
        )

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

        entry_image_1 = PhotoImage(
            file=self.relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            540.0,
            249.5,
            image=entry_image_1
        )
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

        entry_image_2 = PhotoImage(
            file=self.relative_to_assets("entry_2.png"))
        entry_bg_2 = canvas.create_image(
            540.0,
            106.5,
            image=entry_image_2
        )
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

        login_button_image = PhotoImage(
            file=self.relative_to_assets("button_1.png"))
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

        registation_button_image = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
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
