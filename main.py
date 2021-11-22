import cv2
import numpy as np
import time
from grid import Grid
from solver import Sudoku
from process import *


def main():
    # vid = cv2.VideoCapture("D:\Projects\Sudoku\images\ec.mp4")
    # if (vid.isOpened() == False):
    #     print("Error opening video stream or file")
    #
    # start_time = time.time()
    # while(vid.isOpened()):
    #     ret, frame = vid.read()
    #     if ret:
    #         frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
    #         frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    #         image = processImg(frame)
    #         image = removeGrid(image)
    #
    #         try:
    #             # grid = Grid(image)
    #             # grid.iterCell()
    #             # print(grid.getSudoku())
    #             # solver = Sudoku(sudoku)
    #             # if solver.solve(0,0):
    #             #     print(solver.getSolved())
    #             #     imgText = putNum(image.copy(), solver.getSolved(), grid.getGridCoord())
    #             #     cv2.imshow('text', imgText)
    #             # else:
    #             #     print('No Solution')
    #             cv2.imshow('frame', frame)
    #             cv2.imshow('Warped', image)
    #
    #         except:
    #             print('--------------------------------------------')
    #         cv2.imshow('frame', frame)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #         print("Time taken by th loop: {}".format(time.time() - start_time))
    #         start_time = time.time()
    #     else:
    #         break
    # vid.release()
    # cv2.destroyAllWindows()

    img = cv2.imread("D:\Projects\Sudoku\images\img1.jpg")
    print('--->Image loaded...')
    image = processImg(img)  # Preprocessing image to a binary image (threshInv)
    image = removeGrid(image)  # Removing the grid lines
    print('--->Image processed...')
    grid = Grid(image)  # Creating Grid object
    grid.iterCell()
    sudoku = grid.getSudoku()
    print('--->Sudoku detected...')
    solver = Sudoku(sudoku)
    if solver.solve(0,0):
        print('--->Sudoku solved...')
        # print(solver.getSolved())
        imgText = putNum(image.copy(), solver.getSolved(), grid.getGridCoord())
        final = reverseWarp(imgText, img)
        cv2.imshow("original", img)
        cv2.imshow("solved", final)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('No Solution')


if __name__ == '__main__':
    main()
