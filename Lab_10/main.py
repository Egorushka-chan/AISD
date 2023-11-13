import os
import random
import tkinter.messagebox
from tkinter import *
from tkinter.ttk import Combobox
from collections import deque

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

BOARD_PLAYER_TYPE = {
    True: 'X',
    False: 'O'
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
                button = Button(buttons_canvas, font=('Inter', 16 * -1),
                                command=lambda _x=x, _y=y: self.press(_x, _y))
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

        # TODO: вывод рассчётов
        # self.window.geometry("1260x614")
        self.window.geometry("910x614")
        self.window.configure(bg="#FFFFFF")

        self.window.iconbitmap(relative_to_assets("icon.ico"))

        self.game_handler = None

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
            'Стандартная - 3 хода вперед',
            'Тяжелая - 10 шагов (только 3x3)'
        )

        self.combobox_difficulty = Combobox(self.window, font=("Inter", 16 * -1), values=values, state='readonly')
        self.combobox_difficulty.place(
            x=50,
            y=240,
        )

        self.combobox_difficulty.bind('<<ComboboxSelected>>', self.difficulty_change)
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

        self.y_label = Label(canvas, text="O", font=("Inter", 14 * -1), bg="#FFFFFF")
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
        self.is_show_analysis.set(False)

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

    def difficulty_change(self, x):
        diff_int = self.combobox_difficulty.current()
        if diff_int == 2:
            self.combobox_vertical.current(0)
            self.combobox_horizontal.current(0)

    def play_button_click(self):
        x_max = self.combobox_horizontal.current() + 3
        y_max = self.combobox_vertical.current() + 3
        self.new_board(x_max=x_max, y_max=y_max)

        self.game_handler = GameHandler(self)
        self.game_handler.new_game(x_max=x_max, y_max=y_max)

    def change_current_step(self, number):
        self.move_label['text'] = f'Ход {number}'

    def change_current_side(self, side):
        font_not = ("Inter", 14 * -1)
        font_now = ("Inter", 16 * -1, 'bold')
        if side:
            self.x_label.config(font = font_now)
            self.y_label.config(font = font_not)
        else:
            self.x_label.config(font=font_not)
            self.y_label.config(font=font_now)

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
        if self.game_handler is not None:
            result = self.game_handler.place(x, y)

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
        self.step = 1
        self.game_engine: GameEngine = None
        self.is_game_over = False
        self.mode = None
        self.is_x_moving = True
        self.is_analysis = None

    def new_game(self, x_max, y_max):
        mode = '2pl'
        diff = None
        mode = 'ai'
        if self.window.game_var.get() == 1:
            diff_int = self.window.combobox_difficulty.current()
            diff = 'medium'
            if diff_int == 0:
                diff = 'easy'
            elif diff_int == 1:
                diff = 'medium'
            elif diff_int == 2:
                diff = 'hard'

        elif self.window.game_var.get() == 2:
            mode = '2pl'

        self.game_engine = GameEngine(x_max, y_max, mode, self.window.is_show_analysis.get(), diff)
        self.mode = mode
        if diff is not None:
            self.game_engine.difficulty = diff
        self.is_analysis = self.window.is_show_analysis.get()
        self.is_game_over = False
        self.window.change_current_step(1)
        self.window.change_current_side(True)

    def place(self, x: int, y: int):
        if (self.game_engine is not None) and (self.is_game_over is False):
            r = self.game_engine.place(x, y)
            if r == -1:
                return
            sign = BOARD_PLAYER_TYPE[self.is_x_moving]
            self.window.board.place(x, y, sign)
            self.is_x_moving = not self.is_x_moving
            if (r == 'X') or (r == 'O'):
                winner = 'сторона O'
                if r == 'X':
                    winner = 'сторона X'
                tkinter.messagebox.showinfo('Конец матча!', f'Победитель - {winner}! Хороший раунд')
                self.is_game_over = True
            elif r == 'f':
                tkinter.messagebox.showinfo('Конец матча!', 'Ничья! Хороший раунд')
                self.is_game_over = True
            elif self.mode == 'ai':
                x, y, res = self.game_engine.get_move()
                self.window.board.place(x + 1, y + 1, BOARD_PLAYER_TYPE[self.is_x_moving])
                self.is_x_moving = not self.is_x_moving
                if res != 0:
                    if res == 'f':
                        tkinter.messagebox.showinfo('Конец матча!', 'Ничья! Хороший раунд')
                        self.is_game_over = True
                    else:
                        winner = 'сторона O'
                        if res == 1:
                            winner = 'сторона X'
                        tkinter.messagebox.showinfo('Конец матча!', f'Победитель - {winner}! Хороший раунд')
                        self.is_game_over = True
                else:
                    if self.is_x_moving:
                        self.step = self.step + 1
                    self.window.change_current_step(self.step)
            else:
                if self.is_x_moving:
                    self.step = self.step + 1
                self.window.change_current_step(self.step)
                self.window.change_current_side(self.is_x_moving)


class GameEngine:
    def __init__(self, x_max, y_max, mode, analysys, difficulty):
        self.map = [[' ' for i in range(y_max)] for j in range(x_max)]
        self.is_x_moving = True
        self.difficulty = difficulty
        self.depth = 3
        if difficulty == 'hard':
            self.depth = 10

        self.move_count = 1
        self.x_max = x_max
        self.y_max = y_max

        self.is_active_tree = True
        if ((mode == '2pl') or (difficulty == 'easy')) and not analysys:
            self.is_active_tree = False

        self.node_tree: NodeTree = None

    def create_node_tree(self, depth, side):
        super_node = Node(self.map, side)
        self.node_tree = NodeTree(self, super_node, depth)

    def get_move(self):
        x = 1
        y = 1
        if self.difficulty == 'easy':
            empty_cells = []
            for x in range(self.x_max):
                for y in range(self.y_max):
                    if self.map[x][y] == ' ':
                        empty_cells.append((x, y))
            if empty_cells:
                x, y = random.choice(empty_cells)
                self.map[x][y] = BOARD_PLAYER_TYPE[self.is_x_moving]
                self.is_x_moving = not self.is_x_moving
                if self.is_active_tree:
                    self.node_tree.make_move(self.map)
        else:
            x, y = self.node_tree.get_move()
            self.map[x][y] = BOARD_PLAYER_TYPE[self.is_x_moving]
            self.is_x_moving = not self.is_x_moving
        check = self.check_win()
        return x, y, check

    def place(self, x, y):
        b = self.make_step(x - 1, y - 1, self.map.copy())
        if b != -1:
            self.map = b
            if self.is_active_tree:
                if self.node_tree is None:
                    self.create_node_tree(self.depth, self.is_x_moving)
                else:
                    self.node_tree.make_move(b)
            win = self.check_win()
            if win == 1:
                return 'X'
            elif win == -1:
                return 'O'
            elif win == 'f':
                return 'f'
        else:
            print('Поле уже занято')
            return -1

    def make_step(self, x: int, y: int, board):
        curr_value = board[x][y]
        if curr_value == ' ':
            board[x][y] = BOARD_PLAYER_TYPE[self.is_x_moving]
            self.is_x_moving = not self.is_x_moving
            return board
        else:
            return -1

    def check_win(self):
        node = Node(self.map, self.is_x_moving)
        node_tree = NodeTree(self, node, 0)
        victory_X = node_tree.check_win(node, True)
        victory_O = node_tree.check_win(node, False)

        board = node.map
        full = True
        for x_lines in board:
            if " " in x_lines:
                full = False

        if victory_X and not victory_O:
            return 1
        elif victory_O and not victory_X:
            return -1
        elif full:
            return 'f'
        else:
            return 0


class NodeTree:
    def __init__(self, game_engine, super_node, depth):
        self.super_node: Node = super_node
        self.game_engine = game_engine
        self.depth = depth
        self.create_child_nodes(super_node, depth)

    def create_child_nodes(self, node, depth):
        nodes_to_parting = deque()
        nodes_to_parting.append((node, depth))

        while nodes_to_parting:
            curr_node, depth = nodes_to_parting.popleft()
            if depth != 0:
                for x in range(curr_node.x):
                    for y in range(curr_node.y):
                        if curr_node.map[x][y] == ' ':
                            copy_map = curr_node.copy_map()
                            copy_map[x][y] = BOARD_PLAYER_TYPE[curr_node.step]
                            new_node = Node(copy_map, not curr_node.step, curr_node)
                            nodes_to_parting.append((new_node, depth - 1))
                            curr_node.child_nodes.append(new_node)

    def make_move(self, map):
        for child_node in self.super_node.child_nodes:
            if child_node.compare_map(map):
                self.super_node = child_node
                self.expand_node(child_node)
                return
        else:
            print('Ошибка: Ход не в области минимакса')

    def calculate_minimax_weight(self, node):
        if len(node.child_nodes) != 0:
            score = self.estimate(node)
            if score != 0:
                node.weight = score
                node.end = True
                return node.weight

            favorite_node: Node = node.child_nodes[0]
            for child_node in node.child_nodes:
                self.calculate_minimax_weight(child_node)

            for child_node in node.child_nodes:
                if node.step:
                    if favorite_node.weight < child_node.weight:
                        favorite_node = child_node
                else:
                    if favorite_node.weight > child_node.weight:
                        favorite_node = child_node
            node.weight = favorite_node.weight
            return favorite_node.weight
        else:
            score = self.estimate(node)
            node.weight = score
            return node.weight

    def calculate_average_weight(self, node):
        if len(node.child_nodes) != 0:
            score = self.estimate(node)
            if score != 0:
                node.weight = score
                node.end = True
                return node.weight

            favorite_node: Node = node.child_nodes[0]
            for child_node in node.child_nodes:
                score = self.calculate_average_weight(child_node)
                favorite_node.weight = (score + favorite_node.weight) / 2
            node.weight = favorite_node.weight
            return favorite_node.weight
        else:
            score = self.estimate(node)
            node.weight = score
            return node.weight

    def get_move(self):
        side = self.super_node.step
        self.calculate_minimax_weight(self.super_node)
        favorite_node = self.super_node.child_nodes[0]
        for child_node in self.super_node.child_nodes:
            if side:
                if favorite_node.weight < child_node.weight:
                    favorite_node = child_node
            else:
                if favorite_node.weight > child_node.weight:
                    favorite_node = child_node

        # if favorite_node.weight == 0:
        #     favorite_node = random.choice(self.super_node.child_nodes)

        for x in range(favorite_node.x):
            for y in range(favorite_node.y):
                if favorite_node.map[x][y] != self.super_node.map[x][y]:
                    self.make_move(favorite_node.map)
                    return x, y

    def check_win(self, node, side):
        default_moves = [(-1, -1), (0, -1), (-1, 0), (1, 0), (1, 1), (0, 1), (1, -1), (-1, 1)]
        places = []
        board = node.map

        y_lines = 0
        x_lines = len(board)
        for i in range(x_lines):
            y_lines = len(board[i])
            for j in range(y_lines):
                if BOARD_PLAYER_TYPE[side] == board[i][j]:
                    places.append((i, j))

        for direction in default_moves:
            dir_x, dir_y = direction
            for place in places:
                place_x, place_y = place
                fin_x = place_x + dir_x
                fin_y = place_y + dir_y
                if ((fin_x >= 0) and (fin_y >= 0)) and ((fin_x < x_lines) and (fin_y < y_lines)):
                    check_positions = deque()
                    check_positions.append((fin_x, fin_y, (node.x - 1, node.y - 1)))

                    while check_positions:
                        res = check_positions.pop()
                        test_x = res[0]
                        test_y = res[1]
                        win_xs, win_ys = res[2]
                        if board[test_x][test_y] == BOARD_PLAYER_TYPE[side]:
                            win_xs -= abs(dir_x)
                            win_ys -= abs(dir_y)
                            fin_x = test_x + dir_x
                            fin_y = test_y + dir_y
                            if ((fin_x >= 0) and (fin_y >= 0)) and ((fin_x < x_lines) and (fin_y < y_lines)):
                                check_positions.append((fin_x, fin_y, (win_xs, win_ys)))
                        if (win_ys < 1) or (win_xs < 1):
                            return True

    def estimate(self, node):
        board = node.map
        full = True
        for x_lines in board:
            if " " in x_lines:
                full = False

        if self.check_win(node, True):
            return 1
        elif self.check_win(node, False):
            return -1
        elif full:
            return 0
        else:
            return 0

    def expand_node(self, child_node):
        passing_throw_nodes = deque()
        operating_nodes = []
        for child in child_node.child_nodes:
            passing_throw_nodes.append((child, self.depth - 2))
            while passing_throw_nodes:
                ps_node, depth = passing_throw_nodes.popleft()
                if depth != 0:
                    for child in ps_node.child_nodes:
                        passing_throw_nodes.append((child, depth - 1))
                else:
                    operating_nodes.append(ps_node)

        for op_node in operating_nodes:
            self.create_child_nodes(op_node, 1)
            pass


class Node:
    def __init__(self, map, step, parent=None, end=False):
        self.parent_node = parent
        self.child_nodes = []
        self.map = map
        self.x = len(map)
        self.y = len(map[0])
        self.weight = 0
        self.step = step
        self.end = end

    def copy_map(self):
        x_len = len(self.map)
        y_len = len(self.map[0])
        return_map = [[' ' for i in range(x_len)] for j in range(y_len)]
        for x in range(x_len):
            for y in range(y_len):
                return_map[x][y] = self.map[x][y]
        return return_map

    def compare_map(self, map):
        is_equal = True
        for x in range(self.x):
            for y in range(self.y):
                if map[x][y] != self.map[x][y]:
                    is_equal = False
                    return is_equal
        return is_equal


if __name__ == "__main__":
    GameWindow()
