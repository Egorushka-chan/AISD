from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


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

        button_image_1 = PhotoImage(
            master=window,
            file=self.relative_to_assets("button_1.png"))
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

        self.controller = controller
        self.controller.loginForm.close()
        window.resizable(False, False)
        window.mainloop()

    def relative_to_assets(self, path: str):
        return self.path + r'/mainForm/' + path
