import time
class Sudoku:
    def __init__(self, s):
        self.s = s

    def display(self):
        for i in range(9):
            for j in range(9):
                print(self.s[i][j], sep=" ", end=" ")
            print()

    def checkColumn(self, x, y, num):
        for i in range(9):
            if self.s[i][y] == num:
                return 1
        return 0

    def checkRow(self, x, y, num):
        for i in range(9):
            if self.s[x][i] == num:
                return 1
        return 0

    def checkSquare(self, x, y, num):
        i = 0
        j = 0
        if x < 3:
            i = 0
        elif x < 6:
            i = 3
        else:
            i = 6
        if y < 3:
            j = 0
        elif y < 6:
            j = 3
        else:
            j = 6
        for ti in range(i, i + 3):
            for ty in range(j, j + 3):
                if self.s[ti][ty] == num:
                    return 1
        return 0

    def solve(self, x, y):
        num = 1
        if self.s[x][y] != 0:
            if x == 8 and y == 8:
                return 1
            if x < 8:
                x = x + 1
            else:
                x = 0
                y = y + 1
            if self.solve(x, y) == 1:
                return 1
            else:
                return 0
        if self.s[x][y] == 0:
            while (num < 10):
                if self.checkColumn(x, y, num) == 0 and self.checkRow(x, y, num) == 0 and self.checkSquare(x, y,
                                                                                                           num) == 0:  # and checkAdj(x,y,num)==0 :
                    self.s[x][y] = num
                    if x == 8 and y == 8:
                        return 1
                    if x < 8:
                        tx = x + 1
                        ty = y
                    else:
                        tx = 0
                        ty = y + 1
                    if self.solve(tx, ty) == 1:
                        return 1
                num = num + 1
            self.s[x][y] = 0
            return 0

    def getSolved(self):
        return self.s

if __name__ == '__main__':

    s = [[0, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 8, 0, 0, 0, 7, 0, 9, 0],
    [6, 0, 2, 0, 0, 0, 5, 0, 0],
    [0, 7, 0, 0, 6, 0, 0, 0, 0],
    [0, 0, 0, 9, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 4, 0],
    [0, 0, 5, 0, 0, 0, 6, 0, 3],
    [0, 9, 0, 4, 0, 0, 0, 7, 0],
    [0, 0, 6, 0, 0, 0, 0, 0, 0]]

    start_time = time.time()

    sudoku = Sudoku(s)
    if (sudoku.solve(0, 0)):
        sudoku.display()
    else:
        print('!!!!!!!!!!!')
    print("Run time: %s seconds" % (time.time() - start_time))