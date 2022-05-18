class Matrix:
    def __init__(self, n, m, unit_m=False):
        self.n = n
        self.m = m
        self.matrix = []
        for i in range(n):
            self.matrix.append([])
            for j in range(m):
                if j == i and unit_m:
                    self.matrix[i].append(1)
                else:
                    self.matrix[i].append(0)

    def __str__(self):
        matrix = ''
        for i in range(self.n):
            for j in range(self.m):
                matrix += str(self.matrix[i][j]) + ' '
            matrix += '\n'
        return matrix

    def __add__(self, other):
        res = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                res.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]
        return res

    def __sub__(self, other):
        res = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                res.matrix[i][j] = self.matrix[i][j] - other.matrix[i][j]
        return res

    def __mul__(self, other):
        if self.m == other.n:
            res = Matrix(self.n, other.m)
            for i in range(res.n):
                for j in range(res.m):
                    for r in range(other.n):
                        res.matrix[i][j] += self.matrix[i][r] * other.matrix[r][j]
            return res

    def __rmul__(self, other):
        res = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                res.matrix[i][j] = self.matrix[i][j] * other
        return res

    def __truediv__(self, other):
        res = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                res.matrix[i][j] = self.matrix[i][j] / other
        return res


def transpose(matrix):
    res = Matrix(matrix.m, matrix.n)
    for i in range(matrix.m):
        for j in range(matrix.n):
            res.matrix[i][j] = matrix.matrix[j][i]
    return res


def inverse(matrix):
    return 1 / det_g(matrix) * transpose(mat_alg_add(matrix))


def mat_alg_add(matrix):
    min_mat = Matrix(matrix.n, matrix.m)
    for i in range(matrix.n):
        for j in range(matrix.m):
            min_mat.matrix[i][j] = (-1) ** (i + 1 + j + 1) * det_g(minor(matrix, i, j))
    return min_mat


def det_g(matrix):
    k_d = 1
    n = len(matrix.matrix)
    matrix_clone = Matrix(n, n)
    for i in range(n):
        for j in range(n):
            matrix_clone.matrix[i][j] = matrix.matrix[i][j]
    if matrix_clone.matrix[0][0] != 1 and matrix_clone.matrix[0][0] != 0:
        k_d = matrix_clone.matrix[0][0]
        matrix_clone = matrix_clone / k_d
    for j in range(n):
        for i in range(n):
            if i > j and matrix_clone.matrix[i][j] != 0:
                k = matrix_clone.matrix[i][j] / matrix_clone.matrix[j][j]
                for p in range(j, n):
                    matrix_clone.matrix[i][p] = matrix_clone.matrix[i][p] - k * matrix_clone.matrix[j][p]
    det = k_d
    for j in range(n):
        for i in range(n):
            if i == j:
                det *= matrix_clone.matrix[i][j]

    return det


def det(matrix):
    if len(matrix.matrix) == 2:
        d = matrix.matrix[0][0] * matrix.matrix[1][1] - matrix.matrix[0][1] * matrix.matrix[1][0]
        return d

    if len(matrix.matrix) == 3:
        d = matrix.matrix[0][0] * matrix.matrix[1][1] * matrix.matrix[2][2] + \
            matrix.matrix[1][0] * matrix.matrix[0][2] * matrix.matrix[2][1] + \
            matrix.matrix[0][1] * matrix.matrix[1][2] * matrix.matrix[2][0] - \
            matrix.matrix[0][2] * matrix.matrix[1][1] * matrix.matrix[2][0] - \
            matrix.matrix[0][0] * matrix.matrix[1][2] * matrix.matrix[2][1] - \
            matrix.matrix[0][1] * matrix.matrix[1][0] * matrix.matrix[2][2]
        return d

    d = 0

    for j in range(matrix.m):
        if matrix.matrix[0][j] != 0:
            d = d + ((-1) ** (1 + j + 1)) * matrix.matrix[0][j] * det(minor(matrix, 0, j))
    return d


def minor(matrix, row, col):
    minor = Matrix(matrix.n, matrix.m)
    for i in range(minor.n):
        for j in range(minor.m):
            minor.matrix[i][j] = matrix.matrix[i][j]
    minor.matrix.pop(row)
    minor.n -= 1
    for i in range(minor.n):
        for j in range(minor.m):
            if j == col:
                minor.matrix[i].pop(j)
                continue
    minor.m -= 1
    return minor


def matrix_from_file(file_name):
    f = open(file_name, 'r')
    nm = f.readline().split()
    n = int(nm[0])
    m = int(nm[1])
    mat = Matrix(n, m)
    rows = f.readlines()[0:]
    for i in range(n):
        for j in range(m):
            mat.matrix[i][j] = int(rows[i].split()[j])
    return mat
