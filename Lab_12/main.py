import decimal
from decimal import Decimal as Dec
import random
import numpy as np


def calculate(x, sign, t):
    n = 1
    factorial = 1
    result: Dec = Dec(0)
    nummed_x = x  # обозначает x в степени n
    while True:
        current_value = sign * Dec(np.linalg.det(nummed_x) / factorial)
        result += current_value

        if abs(current_value) < (1 / (10 ** t)):
            break
        n += 1
        sign *= (-1)
        factorial *= n
        nummed_x *= n
    return result


if __name__ == "__main__":
    try:
        print('Введите значение t, которое определяет количество знаков после запятой')
        t = int(input('ВВОД = '))
        decimal.getcontext().prec = t

        sign = -1
        if random.random() == 1:  # либо 0, либо 1
            sign = 1
            print('Знак первого слагаемого это +')
        else:
            print('Знак первого слагаемого это -')

        k = random.randint(3, 10)  # ранг матрицы
        x = np.random.randint(-10, 10, (k, k))
        while np.linalg.matrix_rank(x) != k:
            x = np.random.randint(1, 10, (k, k))

        print('Сгенерирована матрица x')
        print(x)
        print(f'Ранг матрицы {k}')
        print(f'Определитель матрицы {np.linalg.det(x)}')

        result = calculate(x, sign, t)

        print(f"Результат: {result:.{t}f}")  # форматирует

    except ValueError:
        print('Неправильно введенное значение. Перезапустите скрипт')
