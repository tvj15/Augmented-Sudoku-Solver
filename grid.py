import cv2
import numpy as np
from keras.models import load_model

model = load_model('D:\Projects\Sudoku\CNN\model.h5')


class Grid:
    def __init__(self, image):
        self.image = image
        self.width = self.image.shape[1]
        self.height = self.image.shape[0]
        self.sqr = self.height // 9
        self.sudoku = np.zeros([9, 9], dtype='int8')
        self.gridCoord = []
        for i in range(0, self.height, self.sqr):
            t = []
            for j in range(0, self.width, self.sqr):
                t.append({'pos':(i,j), 'fix':None})
            if len(self.gridCoord) != 9:
                self.gridCoord.append(t)

    def iterCell(self):
        for i in range(0, 9):
            for j in range(0, 9):
                x, y = self.gridCoord[i][j]['pos']
                cell = self.image[x:x + self.sqr, y:y + self.sqr]
                n, p = self.predDigit(cell)
                self.sudoku[i][j] = n
                if n == 0:
                    self.gridCoord[i][j]['fix'] = False
                else:
                    self.gridCoord[i][j]['fix'] = True
                # print(str(n) + ' : (' + str(p) + ')')
                # cv2.imshow("cell", cell)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

    def predDigit(self, cell):
        cell = cell / 255.0
        pred = model.predict(cell.reshape(1, 28, 28, 1))
        if max(pred[0])*100 > 70:
            return np.argmax(pred), max(pred[0]) * 100
        else:
            return 0, 0


    def getSudoku(self):
        return self.sudoku

    def getGridCoord(self):
        return self.gridCoord