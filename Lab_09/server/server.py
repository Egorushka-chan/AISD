import socket
import enum
import csv
import time

HOST = '127.0.0.1'
PORT = 9090

class Client:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.type = None


class ClientHeader(enum.Enum):
    Closed = 0
    Authorisation = 1
    Registration = 2


class Server:
    def __init__(self):
        self.addr = (HOST, PORT)
        self.sock = socket.create_server(self.addr)

        self.clients = []

        print('Server started')

        self.checking_sockets = False

        timing = time.time()
        while True:
            if time.time() - timing > 1:
                timing = time.time()
                self.check_sockets()

    def check_sockets(self):
        if self.checking_sockets:
            return
        self.checking_sockets = True

        self.sock.settimeout(0.5)
        try:
            conn, addr = self.sock.accept()
            self.clients.append(Client(conn, addr))
            print('Connected ', addr)
        except:
            pass

        for x in self.clients:
            self.check_client_for_message(x)

        self.checking_sockets = False

        print('Текущие подключения:')
        for x in self.clients:
            print(x.address)

    def check_client_for_message(self, client):
        try:
            data = client.socket.recv(1024).decode('utf-8')
            if data == b'':
                raise Exception()
        except Exception as ex:
            print(f'{client.address} неожиданно отключился: {ex}')
            self.clients.remove(client)
            return
        if data:
            header_type = ClientHeader(int(data[0]))
            if header_type == ClientHeader.Registration:
                print(f'{client.address}: запрос на регистрацию')
                _, login, password, name = data.split(';')
                existing_user = self.find_user(login, password)
                if not existing_user:
                    result = self.create_user(login, password, name)
                    if result:
                        client.socket.send(bytes('1;Запрос на регистрацию успешен', encoding='utf-8'))
                        print(f'{client.address}: Создан новый пользователь {name}')
                    else:
                        client.socket.send(bytes(f'2;{result}', encoding='utf-8'))
                        print(f'{client.address}: регистрация провалена')
            elif header_type == ClientHeader.Authorisation:
                self.authorisation(client, data)
            elif header_type == ClientHeader.Closed:
                print(f'{client.address} отключился')
                self.clients.remove(client)
                return
            else:
                print(f'{client.address}: неизвестный заголовок')

    def authorisation(self, client, data):
        print(f'{client.address}: запрос на авторизацию')
        _, login, password = data.split(';')
        result = self.find_user(login, password)
        if not result:
            client.socket.send(b'2')
            print(f'{client.address}: неправильные данные')
        else:
            client.socket.send(bytes(f'1;{login};{result[3]};{result[4]}', encoding='utf-8'))
            print(f'{client.address}: успешно авторизован')

    def find_user(self, login, password):
        with open('users.csv', 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                if (row[1].strip() == login) and (row[2].strip() == password):
                    return row
            return False

    def create_user(self, login, password, name):
        try:
            with open('users.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(
                    (
                        3,
                        login,
                        password,
                        name,
                        0
                    )
                )
        except Exception as ex:
            return ex
        return True


if __name__ == '__main__':
    Server()
