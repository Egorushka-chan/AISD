from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


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

        button_image_1 = PhotoImage(
            master=self.window,
            file=self.relative_to_assets("button_1.png"))
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

        entry_image_1 = PhotoImage(
            master=self.window,
            file=self.relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            166.0,
            92.0,
            image=entry_image_1
        )
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

        entry_image_2 = PhotoImage(
            master=self.window,
            file=self.relative_to_assets("entry_2.png"))
        entry_bg_2 = canvas.create_image(
            166.0,
            209.0,
            image=entry_image_2
        )
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

        entry_image_3 = PhotoImage(
            master=self.window,
            file=self.relative_to_assets("entry_1.png"))
        entry_bg_3 = canvas.create_image(
            167.0,
            326.0,
            image=entry_image_3
        )
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
    
    def close(self):
        self.window.destroy()
