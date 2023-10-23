import os
from tkinter import *
from tkinter.ttk import Combobox

ASSETS_PATH = os.path.dirname(os.path.realpath(__file__)) + r"\assets"


def relative_to_assets(path: str, filetype=r'/images/'):
    return ASSETS_PATH + filetype + path


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


class Board(Frame):
    def __init__(self, master, width, height, movement_method, x_max=3, y_max=3, *args, **kwargs):
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
                button = Button(buttons_canvas, text=f'{BOARD_VERTICAL_HEADERS[y]}{x}',
                                command=lambda _x=x, _y=y: self.press(_x, BOARD_VERTICAL_HEADERS[_y]))
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
        self.create_static_markup(canvas)

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
            'Сложная - 3 хода вперед'
        )

        self.combobox_difficulty = Combobox(self.window, font=("Inter", 16 * -1), values=values, state='readonly')
        self.combobox_difficulty.place(
            x=50,
            y=240,
        )

        self.combobox_difficulty.current(1)

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
            width=500,
            height=500
        )

        self.board = None
        self.new_board(x_max=3, y_max=3)

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

        values_vert = (
            "C: 3 линии",
            'D: 4 линии',
            'E: 5 линий',
            'F: 6 линий',
            'G: 7 линий',
            'H: 8 линий'
        )

        self.combobox_vertical = Combobox(self.window, font=("Inter", 16 * -1), values=values_vert, state='readonly')
        self.combobox_vertical.place(
            x=23,
            y=453,
            width=252 - 23,
            height=489 - 453
        )

        self.combobox_vertical.current(0)

        values_horizontal = (
            "3 линии",
            '4 линии',
            '5 линий',
            '6 линий',
            '7 линий',
            '8 линий'
        )

        self.combobox_horizontal = Combobox(self.window, font=("Inter", 16 * -1), values=values_horizontal,
                                            state='readonly')
        self.combobox_horizontal.place(
            x=23,
            y=539,
            width=252 - 23,
            height=575 - 539
        )

        self.combobox_horizontal.current(0)

        self.is_show_analysis = BooleanVar(self.window)
        self.is_show_analysis.set(True)

        Checkbutton(canvas, text='Показывать расчёты', font=("Inter", 16 * -1), bg="#EEEEEE",
                    variable=self.is_show_analysis, onvalue=1, offvalue=0, ).place(
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
        diff_int = self.combobox_difficulty.current()
        diff = 'medium'
        if diff_int == 0:
            diff = 'easy'
        elif diff_int == 1:
            diff = 'medium'
        elif diff_int == 2:
            diff = 'hard'

        x_max = self.combobox_horizontal.current() + 3
        y_max = self.combobox_vertical.current() + 3

        self.new_board(x_max, y_max)

    def new_board(self, x_max, y_max):
        if self.board is not None:
            self.board.destroy()
        self.board = Board(self.board_frame, movement_method=self.board_click,
                           width=500,
                           height=500,
                           x_max=x_max,
                           y_max=y_max)
        self.board.pack()

    def board_click(self, x, y):
        print(f'button x:{x} y:{y} clicked')

    def create_static_markup(self, canvas):  # для уменьшения размера init
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

        canvas.create_text(
            23.0,
            139,
            anchor="nw",
            text="Режим игры:",
            fill="#000000",
            font=("Inter", 16 * -1, 'bold')
        )

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

        canvas.create_text(
            1049.0,
            16,
            anchor="nw",
            text="Анализ",
            fill="#000000",
            font=("Inter", 20 * -1, 'bold')
        )

        canvas.create_text(
            592.0,
            555.0,
            anchor="nw",
            text="|",
            fill="#000000",
            font=("Inter", 16 * -1, 'bold')
        )

        canvas.create_text(
            23.0,
            391,
            anchor="nw",
            text="Размер доски:",
            fill="#000000",
            font=("Inter", 16 * -1, "bold")
        )

        canvas.create_text(
            23.0,
            426,
            anchor="nw",
            text="A",
            fill="#000000",
            font=("Inter", 16 * -1)
        )

        canvas.create_text(
            238.0,
            426,
            anchor="nw",
            text="H",
            fill="#000000",
            font=("Inter", 16 * -1)
        )

        canvas.create_text(
            94.0,
            426,
            anchor="nw",
            text="Вертикали",
            fill="#000000",
            font=("Inter", 16 * -1)
        )

        canvas.create_text(
            23.0,
            512,
            anchor="nw",
            text="1",
            fill="#000000",
            font=("Inter", 16 * -1)
        )

        canvas.create_text(
            238.0,
            512,
            anchor="nw",
            text="8",
            fill="#000000",
            font=("Inter", 16 * -1)
        )

        canvas.create_text(
            86.0,
            512,
            anchor="nw",
            text="Горизонтали",
            fill="#000000",
            font=("Inter", 16 * -1)
        )

        canvas.create_rectangle(
            44.0,
            436,
            84.0,
            436,
            fill="#000000",
            outline="")

        canvas.create_rectangle(
            189,
            436,
            229,
            436,
            fill="#000000",
            outline="")

        canvas.create_rectangle(
            18.0,
            375,
            241.0,
            375,
            fill="#000000",
            outline="")

        canvas.create_rectangle(
            44.0,
            522.0,
            79.0,
            522.0,
            fill="#000000",
            outline="")

        canvas.create_rectangle(
            192.0,
            522.0,
            232.0,
            522.0,
            fill="#000000",
            outline="")


class GameHandler:
    def __init__(self, window: GameWindow):
        self.window = window
        self.game_engine = None
        self.mode = None

    def new_game(self, mode='ai', difficulty='easy', is_analysis=True):
        pass

    def place(self, x: int, y: int):
        pass

    def game_engine_instance(self):
        if self.game_engine is not None:
            return self.game_engine
        else:
            self.game_engine = GameEngine()
            return self.game_engine


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
