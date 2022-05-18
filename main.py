import math
from numpy import linalg
import matrix as mt


class Class:
    def __init__(self, name):
        self.name = name
        self.sample_list = []  # хранение экземпляров в виде матриц
        self.vector_list = []  # хранение экземпляров в виде списка признаков (В виде столбца матрицы)

    def add_sample(self, sample):
        self.sample_list.append(sample)
        self.vector_list.append(vector_from_matrix(sample))

    def core(self):
        core = mt.Matrix(len(self.sample_list[0].matrix), len(self.sample_list[0].matrix[0]))
        for i in range(core.n):
            for j in range(core.m):
                average = 0
                for sample in self.sample_list:
                    average += sample.matrix[i][j]
                average /= len(self.sample_list)
                core.matrix[i][j] = average
        return core


def load_samples(class1, class2, class3, class4, file_name):  # загрузка и распределение экземпляров из файла
    f = open(file_name)
    while True:
        line = f.readline().split()
        if not line:
            line = f.readline().split()
            if not line:
                break
        if len(line) == 2:
            n = int(line[0])
            m = int(line[1])
            mat = mt.Matrix(n, m)
            for i in range(n):
                line = f.readline().split()
                for j in range(m):
                    mat.matrix[i][j] = int(line[j])
        elif len(line) == 1:
            name = line[0]
            if name == class1.name:
                class1.add_sample(mat)
            if name == class2.name:
                class2.add_sample(mat)
            if name == class3.name:
                class3.add_sample(mat)
            if name == class4.name:
                class4.add_sample(mat)
        else:
            print('Строка не распознана')


def recognize_from_file(class1, class2, class3, class4, file_name):  # распознавание объектов из файла
    f = open(file_name)
    while True:
        line = f.readline().split()
        if not line:
            line = f.readline().split()
            if not line:
                break
        if len(line) == 2:
            n = int(line[0])
            m = int(line[1])
            obj = mt.Matrix(n, m)
            for i in range(n):
                line = f.readline().split()
                for j in range(m):
                    obj.matrix[i][j] = int(line[j])

            print(obj)

            d1 = distance_e_m(class1, obj)
            print(f'Расстояние до класса {class1.name}: {d1}')
            d2 = distance_e_m(class2, obj)
            print(f'Расстояние до класса {class2.name}: {d2}')
            d3 = distance_e_m(class3, obj)
            print(f'Расстояние до класса {class3.name}: {d3}')
            d4 = distance_e_m(class4, obj)
            print(f'Расстояние до класса {class4.name}: {d4}')

            if d1 > 3.5 and d2 > 3.5 and d3 > 3.5 and d4 > 3.5:
                print("Я не знаю что это")
            else:
                min_dist = min(d1, d2, d3, d4)
                if min_dist == d1:
                    print("Это похоже на " + class1.name)
                elif min_dist == d2:
                    print("Это похоже на " + class2.name)
                elif min_dist == d3:
                    print("Это похоже на " + class3.name)
                elif min_dist == d4:
                    print("Это похоже на " + class4.name)
                print('\n\n')
        else:
            print('Строка не распознана')


def distance_e_m(class1, obj):
    x = vector_from_matrix(class1.core())
    y = vector_from_matrix(obj)
    S = covariance_matrix(class1)
    E = mt.Matrix(S.n, S.m, True)
    dist = math.sqrt((mt.transpose(x - y) * from_np_to_mt(linalg.inv((S + E).matrix)) * (x - y)).matrix[0][0])
    return dist


def vector_from_matrix(matrix):  # Возвращает сразу транспонированный вектор ( т.к. 𝑥=(𝑥1,...,𝑥𝑝 )^𝑇 )
    vector = mt.Matrix(matrix.n * matrix.m, 1)
    p = 0
    for i in range(matrix.n):
        for j in range(matrix.m):
            vector.matrix[p][0] = matrix.matrix[i][j]
            p += 1

    return vector


def covariance_matrix(class1):
    c_m = mt.Matrix(len(class1.vector_list[0].matrix), len(class1.vector_list[0].matrix))
    core = vector_from_matrix(class1.core())
    N = len(class1.vector_list)
    for i in range(c_m.n):
        for j in range(c_m.m):
            for k in range(0, N):
                c_m.matrix[i][j] += (1 / (N - 1)) * (class1.vector_list[k].matrix[i][0] - core.matrix[i][0]) * \
                                    (class1.vector_list[k].matrix[j][0] - core.matrix[j][0])

    return c_m


def from_np_to_mt(array):  # преобразование формата матрицы numpy к формату класса Matrix
    mat = mt.Matrix(array.shape[0], array.shape[1])
    for i in range(mat.n):
        for j in range(mat.m):
            mat.matrix[i][j] = array[i][j]
    return mat


A = Class('Letter_A')
B = Class('Letter_B')
C = Class('Letter_C')
D = Class('Letter_D')

load_samples(A, B, C, D, 'samples.txt')
for c in A, B, C, D:
    print(f'Ядро класса {c.name}:')
    print(c.core())
print('Распознаем следующие объекты:\n')
recognize_from_file(A, B, C, D, 'obj_to_recognize.txt')
