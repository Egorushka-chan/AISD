import os
from tkinter import *
from tkinter.ttk import Combobox

ASSETS_PATH = os.path.dirname(os.path.realpath(__file__)) + r"\assets"


def relative_to_assets(path: str, filetype=r'/images/'):
    return ASSETS_PATH + filetype + path


class GameWindow:
    def __init__(self):
        self.window = Tk()
        self.window.title('Крестики-нолики')

        self.window.geometry("1260x614")
        self.window.configure(bg="#FFFFFF")

        self.window.iconbitmap(relative_to_assets("icon.ico"))

        canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=614,
            width=1260,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        canvas.create_rectangle(
            0.0,
            5.6,
            277.0,
            614.0,
            fill="#EEEEEE",
            outline="")

        canvas.create_rectangle(
            912.0,
            5.6,
            1260.0,
            614.0,
            fill="#EEEEEE",
            outline="")

        canvas.create_text(
            51.0,
            21,
            anchor="nw",
            text="Крестики-нолики",
            fill="#000000",
            font=("Inter", 20 * -1, 'bold')
        )

        button_image_1 = PhotoImage(
            file=relative_to_assets("play_button.png"))
        play_button = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.play_button_click,
            relief="flat"
        )
        play_button.place(
            x=34.0,
            y=64,
            width=210.0,
            height=55.0
        )

        canvas.create_text(
            23.0,
            139,
            anchor="nw",
            text="Режим игры:",
            fill="#000000",
            font=("Inter", 16 * -1, 'bold')
        )

        self.game_var = IntVar(self.window)
        self.game_var.set(1)
        self.game_var.trace("w", self.game_var_change)

        radio_computer = Radiobutton(self.window, text='Игра с компьютером', font=("Inter", 16 * -1),
                                     variable=self.game_var, value=1)
        radio_computer.place(
            x=23,
            y=174,
            anchor='nw'
        )

        values = (
            "Легкая  - случайные ходы",
            'Средняя - видит на 1 ход',
            'Непобедимая - не может проиграть'
        )

        self.combobox_difficulty = Combobox(self.window, font=("Inter", 16 * -1), values=values, state='readonly')
        self.combobox_difficulty.place(
            x=50,
            y=240,
        )

        self.combobox_difficulty.current(1)


        canvas.create_rectangle(
            18.0,
            293,
            241.0,
            293,
            fill="#000000",
            outline="")

        canvas.create_text(
            48.0,
            208,
            anchor="nw",
            text="Сложность:",
            fill="#000000",
            font=("Inter", 16 * -1)
        )

        radio_player = Radiobutton(self.window, text='Игра вдвоем', font=("Inter", 16 * -1),
                                   variable=self.game_var, value=2)
        radio_player.place(
            x=23,
            y=322,
            anchor='nw'
        )

        self.board_frame = Frame(canvas, bg="#FFFFFF", borderwidth=1, relief=SOLID)
        self.board_frame.place(
            x=345,
            y=28,
            width=845 - 345,
            height=528 - 28
        )

        canvas.create_text(
            1049.0,
            16,
            anchor="nw",
            text="Анализ",
            fill="#000000",
            font=("Inter", 20 * -1, 'bold')
        )

        self.calc_frame = Frame(canvas, bg='#EEEEEE')
        self.calc_frame.place(
            x=919,
            y=50,
            width=1252 - 919,
            height=567 - 50
        )

        self.move_label = Label(canvas, text="Ход 1", font=("Inter", 16 * -1, 'bold'), bg="#FFFFFF")
        self.move_label.place(
            x=313,
            y=555
        )

        self.x_label = Label(canvas, text="X", font=("Inter", 16 * -1, 'bold'), bg="#FFFFFF")
        self.x_label.place(
            x=487,
            y=555
        )

        self.y_label = Label(canvas, text="O", font=("Inter", 16 * -1, 'bold'), bg="#FFFFFF")
        self.y_label.place(
            x=691,
            y=555
        )

        canvas.create_text(
            592.0,
            555.0,
            anchor="nw",
            text="|",
            fill="#000000",
            font=("Inter", 16 * -1, 'bold')
        )

        self.is_show_analisys = BooleanVar(self.window)
        self.is_show_analisys.set(True)

        Checkbutton(canvas, text='Показывать расчёты', font=("Inter", 16 * -1), bg="#EEEEEE",
                    variable=self.is_show_analisys, onvalue=1, offvalue=0, ).place(
            x=958,
            y=581
        )
        self.window.resizable(False, False)
        self.window.mainloop()

    def game_var_change(self, event=None, trace=None, cmd=None):
        var = self.game_var.get()
        if var == 1:
            self.combobox_difficulty['state'] = 'readonly'
        elif var == 2:
            self.combobox_difficulty['state'] = 'disabled'

    def play_button_click(self):
        print('Play Button Clicked!')


class GameHandler:
    def __init__(self, window: GameWindow):
        pass

    def new_game(self, mode='ai', difficulty='easy'):
        pass

    def place(self, x: int, y: int):
        pass


class GameEngine:
    def __init__(self):
        pass

    def estimate(self):
        pass

    def minimax(self):
        pass

    def get_move(self, side='O'):
        pass


if __name__ == "__main__":
    GameWindow()
