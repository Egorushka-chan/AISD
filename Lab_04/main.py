# Вариант 1:
# Формируется матрица F следующим образом: скопировать в нее А и если количество нулей в В больше, чем в Е, то поменять в
# ней местами В и С симметрично, иначе В и Е поменять местами несимметрично. При этом матрица А не меняется. После чего
# если определитель матрицы А больше суммы диагональных элементов матрицы F, то вычисляется выражение: A*AT – K * F,
# иначе вычисляется выражение (A-1 +G-F-1)*K, где G-нижняя треугольная матрица, полученная из А. Выводятся по мере
# формирования А, F и все матричные операции последовательно.
# D E
# C B

import numpy
import math
from matplotlib import pyplot as plt

try:
    K = int(input('Введите число K = '))
    N = int(input('Введите число N (N>1) = '))
    while N <= 1:
        print('Внимание! Число N должно быть хотя-бы 2!')
        N = int(input('Введите число N (N>1) = '))

    A = numpy.random.randint(-10, 10, (N, N))  # рандомное заполнение
    # A = numpy.array([[int(input(f'(I={i} J={j})= ')) for i in range(N)] for j in range(N)])
    print(f'Изначальная матрица А:\n{A}')

    submatrix_length = N // 2
    x = submatrix_length + N % 2
    D = numpy.array(A[:submatrix_length, :submatrix_length])
    E = numpy.array(A[:submatrix_length, submatrix_length + N % 2:N])
    C = numpy.array(A[submatrix_length + N % 2:N, :submatrix_length])
    B = numpy.array(A[submatrix_length + N % 2:N, submatrix_length + N % 2:N])
    print(f'Субматрицы:\nD{D}\nE{E}\nC{C}\nB{B}')

    F = A.copy()
    print("Создание матрицы F")
    zero_B = numpy.count_nonzero(B == 0)
    zero_E = numpy.count_nonzero(E == 0)
    if zero_B > zero_E:
        print(f'B:{zero_B}>E:{zero_E}. Меняем местами B и C симметрично')
        F[submatrix_length + N % 2:N, :submatrix_length] = B[:submatrix_length, ::-1]  # Вставляем в C
        F[submatrix_length + N % 2:N, submatrix_length + N % 2:N] = C[:submatrix_length, ::-1]  # Вставляем в B
    else:
        print(f'B:{zero_B}≤E:{zero_E}. Меняем местами B и E несимметрично:')
        F[:submatrix_length, submatrix_length + N % 2:N] = B  # Вставляем в E
        F[submatrix_length + N % 2:N, submatrix_length + N % 2:N] = E  # Вставляем в B

    print(f'Итоговая матрица F\n{F}')

    print('Проверяем, что определитель матрицы А больше суммы диагональных элементов матрицы F')
    det_A = numpy.linalg.det(A)
    dia_F = sum(numpy.diagonal(F))
    print(f'Определитель A = {det_A}')
    print(f'Сумма диагональных элементов F = {dia_F}')
    if det_A > dia_F:
        print('Верно. Вычисляем A*AT – K * F')
        result = A * A.transpose() - F * K
        print(f"\nРезультат выражения A*AT – K * F:\n{result}")
    else:
        print('Неверно. Вычисляем (A-1 +G-F-1)*K, где G-нижняя треугольная матрица, полученная из А')
        G = numpy.tri(N) * A
        print(f'Нижняя треугольная матрица G\n{G}')
        result = (numpy.linalg.inv(A) + G - numpy.linalg.inv(F)) * K
        print(f"\nРезультат выражения (A^(-1) + G-F^(-1)) * K:\n{result}")

    fig, ax = plt.subplots(3, 1, figsize=(11, 8))
    plt.suptitle("Создание графиков")

    # Тепловая карта
    ax[0].set(title="Тепловая карта F", xlabel="Номер столбца", ylabel="Номер строки")
    ax[0].imshow(F)
    ax[0].set_xticks(numpy.arange(N), labels=range(N))
    ax[0].set_yticks(numpy.arange(N), labels=range(N))
    [[ax[0].text(i, j, F[j, i], ha="center", va="center", color="w") for i in range(N)] for j in range(N)]
    # Сравнение модулей определителей субматриц
    ax[1].set(title='Сравнение модулей определителей субматриц')
    labels = ['D', 'E', 'C', 'B']
    sizes = []
    sizes.append(abs(numpy.linalg.det(D)))
    sizes.append(abs(numpy.linalg.det(E)))
    sizes.append(abs(numpy.linalg.det(C)))
    sizes.append(abs(numpy.linalg.det(B)))
    ax[1].pie(sizes, labels=labels, autopct='%1.1f%%')
    #Линейчатая диаграмма значения в каждой столбце
    ax[2].set(title='Линейчатая диаграмма значения в каждом столбце')
    rows = [i+1 for i in range(N)]
    values = sum(A)
    ax[2].bar(rows, values)

    plt.tight_layout()
    plt.show()

except ValueError:
    print(f"ValueError - вы неправильно ввели данные.")
except Exception as e:
    print(f'Внимание! Неизв. ошибка: {e}')
