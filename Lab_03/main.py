# С клавиатуры вводится два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц, B,C,D,E
# заполняется случайным образом целыми числами в интервале [-10,10].
# Для тестирования использовать не случайное заполнение, а целенаправленное.

#Вариант №1
# Формируется матрица F следующим образом: если количество нулей в В в области 1 больше, чем в области 3, то поменять в ней
# симметрично области 2 и 4 местами, иначе В и Е поменять местами несимметрично. При этом матрица А не меняется. После чего
# вычисляется выражение: A * AT – K * F. Выводятся по мере формирования А, F и все матричные операции последовательно.

#     4
#  3     1
#     2

#  D E
#  C B
import random
from math import ceil, floor


def print_matrix(matrix):
    for row in matrix:
        print(row)
    print()

def clone_matrix(matrix):
    matrix_new = []  # Клонируем матрицу
    for i in range(N):
        new_row = []
        for j in range(N):
            new_row.append(matrix[i][j])
        matrix_new.append(new_row)
    return matrix_new

try:
    K = int(input('Введите число K: '))
    N = int(input('Введите число  (не меньше 5-и): '))
    while N < 5:
        print('Число N должно быть не менее 5-и. Введите число заново')

    print('Создаем матрицу A:')
    matrix_A = []
    for i in range(N):
        new_row = []
        for j in range(N):
            new_row.append(random.randint(-10, 10))
        matrix_A.append(new_row)

    print_matrix(matrix_A)

    print('Транспонируем матрицу A:')
    matrix_A_trans = []
    for i in range(N):
        new_row = []
        for j in range(N):
            new_row.append(matrix_A[j][i])
        matrix_A_trans.append(new_row)

    print_matrix(matrix_A_trans)

    print('Создаем матрицу F:')

    matrix_F = clone_matrix(matrix_A)

    print('1. Выделяем подматрицу B:')
    B_range = range(ceil(N / 2) - 1, N)
    submatrix_B = []
    for i in B_range:
        new_row = []
        for j in B_range:
            new_row.append(matrix_F[i][j])
        submatrix_B.append(new_row)
    print_matrix(submatrix_B)

    print('2. Считаем нули в областях 1 и 3')

    zero_counter_one = 0
    for i in range(ceil(N / 2)):
        for j in range(ceil(N / 2)):
            if (i <= j) and ((i + j + 1) >= ceil(N / 2)) and submatrix_B[i][j] == 0:
                zero_counter_one += 1

    zero_counter_three = 0
    for i in range(ceil(N/2)):
        for j in range(ceil(N/2)):
            if ((i + j + 1) <= ceil(N/2)) and (i >= j) and submatrix_B[i][j] == 0:
                zero_counter_three += 1

    print(f'Количество нулей в области 1: {zero_counter_one}')
    print(f'Количество нулей в области 3: {zero_counter_three}')

    matrix_F_clone = clone_matrix(matrix_F)
    if zero_counter_one > zero_counter_three:
        print('3. Количество нулей в области 1 больше, чем в области 3, меняем области 2 и 4 симметрично местами')
        for i in range(ceil(N / 2)):
            for j in range(ceil(N / 2)):
                if (i < j) and ((i + j + 1) < ceil(N / 2)):
                    matrix_F[ceil(N / 2) + i][ceil(N / 2) + j] = matrix_F_clone[ceil(N / 2) - i - 1][ceil(N / 2) + j] # во 2 область
                    matrix_F[ceil(N / 2) - i - 1][ceil(N / 2) + j] = matrix_F_clone[ceil(N / 2) + i][ceil(N / 2) + j] # в 4 область
    else:
        print("3. Количество нулей в области 1 меньше или равно количеству нулей в области 3, меняем области B и E местами несимметрично")
        for i in range(ceil(N / 2)):
            for j in range(ceil(N / 2)):
                matrix_F[i][floor(N / 2) + j] = matrix_F_clone[floor(N / 2) + i][floor(N / 2) + j] # в область E значения B
                matrix_F[floor(N / 2) + i][floor(N / 2) + j] = matrix_F_clone[i][floor(N / 2) + j] # в область B значения E

    print('4. Итоговая матрица F:')
    print_matrix(matrix_F)

    print('Умножаем матрицу A на A^-1:')

    result_A_on_A_trans = []
    for i in range(N):
        new_row = []
        for j in range(N):
            new_row.append(0)
        result_A_on_A_trans.append(new_row)

    for i in range(N):
        for j in range(N):
            for c in range(N):
                result_A_on_A_trans[i][j] += matrix_A[i][c] * matrix_A_trans[c][j]

    print_matrix(result_A_on_A_trans)

    print('Умножаем матрицу F на число K:')
    result_F_on_K = []
    for i in range(N):
        new_row = []
        for j in range(N):
            new_row.append(0)
        result_F_on_K.append(new_row)

    for i in range(N):
        for j in range(N):
            result_F_on_K[i][j] += matrix_F[i][j] * K

    print('Итоговая матрица A*AT - K*F')
    result_matrix = []
    for i in range(N):
        new_row = []
        for j in range(N):
            new_row.append(result_A_on_A_trans[i][j] - result_F_on_K[i][j])
        result_matrix.append(new_row)
    print_matrix(result_matrix)
except ValueError:
    print('Вы не правильно ввели данные')
