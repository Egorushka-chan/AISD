import os, socket
from enum import Enum

import forms.mainForm, forms.registrationForm, forms.loginForm


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
        self.model = None
        self.current_user = None

    def open_login(self):
        forms.loginForm.LoginForm(self.assets_path, self)

    def open_registration(self):
        self.registrationForm = forms.registrationForm.RegistrationForm(self.assets_path, self)

    def open_main(self):
        self.mainForm = forms.mainForm.MainForm(self.assets_path, self, self.current_user)

    def send_registration(self, login, password, name):
        try:
            print(login, password, name)
            self.model.send_registration(login, password, name)
        except ConnectionRefusedError as ex:
            self.loginForm.show_error(f'Подключение не удалось: {ex}')
        except AttributeError:
            self.loginForm.show_error('Сервер не запущен')
        except ModuleNotFoundError as ex:
            self.loginForm.show_error(f'Подключение не удалось: {ex}')
        else:
            self.registrationForm.close()


    def send_login(self, login, password):
        try:
            result = self.model.send_login(login, password)
            data = result.split(';')
            self.current_user = User(data[1], data[2], data[3])
        except ConnectionRefusedError as ex:
            self.loginForm.show_error(f'Подключение не удалось: {ex}')
        except AttributeError:
            self.loginForm.show_error('Сервер не запущен')
        except ModuleNotFoundError as ex:
            self.loginForm.show_error(f'Подключение не удалось: {ex}')
        else:
            self.open_main()


class ServerResponseHeader(Enum):
    ServerClose = 0
    Successful = 1
    Failed = 2


class Model:
    def __init__(self):
        self.server_socket = None

    def get_socket(self):
        if self.server_socket is None:
            try:
                self.server_socket = socket.socket()
                self.make_connection()
            except:
                self.server_socket = None
        return self.server_socket

    def make_connection(self):
        self.server_socket.connect(('localhost', 9090))

    def send_registration(self, login, password, name):
        sock = self.get_socket()
        message = '2'
        message += f';{login};{password};{name}'
        sock.send(bytes(message, encoding='utf-8'))

        data = sock.recv(1024).decode('utf-8')
        header = ServerResponseHeader(int(data[0]))
        if header == ServerResponseHeader.Successful:
            return data
        elif header == ServerResponseHeader.Failed:
            raise ModuleNotFoundError('Такой пользователь уже существует')

    def send_login(self, login, password):
        sock = self.get_socket()
        message = '1'
        message += f';{login};{password}'
        sock.send(bytes(message, encoding='utf-8'))

        data = sock.recv(1024).decode('utf-8')
        header = ServerResponseHeader(int(data[0]))

        if header == ServerResponseHeader.Successful:
            return data
        elif header == ServerResponseHeader.Failed:
            raise ModuleNotFoundError('Неправильный логин или пароль')

    def close_connection(self):
        sock = self.get_socket()
        sock.send(b'0')
        sock.close()


if __name__ == '__main__':
    controller = Controller()
    controller.model = Model()
    controller.open_login()

    if controller.model.server_socket is not None:
        controller.model.close_connection()
