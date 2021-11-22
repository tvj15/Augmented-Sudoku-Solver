import numpy as np
import cv2
import time
from keras.models import load_model

model = load_model('D:\Projects\Sudoku\CNN\model.h5')


def processFrame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    threshInv = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 10)
    return threshInv


def findSudoku(img, frame):
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    try:
        sudokuContour = sorted(contours, key=cv2.contourArea, reverse=True)[0]
        epsilon = 0.025 * cv2.arcLength(sudokuContour, True)
        c = cv2.approxPolyDP(sudokuContour, epsilon, True)
        if len(c) > 3:
            # Gets the 4 corners of the object (assume it's a square)
            topLeft = tuple(min(c, key=lambda x: x[0, 0] + x[0, 1])[0])
            bottomRight = tuple(max(c, key=lambda x: x[0, 0] + x[0, 1])[0])
            topRight = tuple(max(c, key=lambda x: x[0, 0] - x[0, 1])[0])
            bottomLeft = tuple(min(c, key=lambda x: x[0, 0] - x[0, 1])[0])
            coord = (topLeft, topRight, bottomLeft, bottomRight)
            cv2.circle(frame, coord[0], 5, (0, 0, 255), -1)
            cv2.circle(frame, coord[1], 5, (0, 0, 255), -1)
            cv2.circle(frame, coord[2], 5, (0, 0, 255), -1)
            cv2.circle(frame, coord[3], 5, (0, 0, 255), -1)
            h = w = 252
            pts1 = np.float32(coord)
            pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            res = cv2.warpPerspective(img, matrix, (w, h))
            return True, res
    except:
        print('Sudoku not found')
    return False, None


def removeGrid(image):
    lines = cv2.HoughLinesP(image, 1, np.pi / 180, 90, minLineLength=100, maxLineGap=50)
    try:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), 0, 5)
    except:
        print('Grid not found')
    return image


def detectNumbers(img):
    for i in range(0, 252, 28):
        for j in range(0, 252, 28):
            cell = img[i:i + 28, j: j + 28]
            contours, _ = cv2.findContours(cell, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            if len(contours) != 0:
                numberContour = sorted(contours, key=cv2.contourArea, reverse=True)[0]
                numberArea = cv2.contourArea(numberContour)
                if numberArea > 25.0:
                    cell = cv2.drawContours(cell, [numberContour], 0, (255))
                    pred = predNumbers(cell)
                    print('({},{}) : {}->{}'.format(i // 28, j // 28, np.argmax(pred), max(pred[0])*100))
                    x, y, w, h = cv2.boundingRect(numberContour)
                    cv2.rectangle(img, (x + j, y + i), (x + w + j, y + h + i), (255))


def predNumbers(cell):
    cell = cell / 255.0
    cell = cell.reshape(1, 28, 28, 1)
    pred = model.predict(cell)
    return pred


def main():
    vid = cv2.VideoCapture('capture.mp4')
    if not vid.isOpened():
        print("Error opening video stream or file")
    else:
        start_time = time.time()
        while (vid.isOpened()):
            ret, frame = vid.read()
            frame = cv2.resize(frame, (frame.shape[1]//3, frame.shape[0]//3))
            proFrame = processFrame(frame)
            check, warped = findSudoku(proFrame, frame)
            if check:
                noGrid = removeGrid(warped)
                detectNumbers(noGrid)
                cv2.imshow('Warped', noGrid)
            else:
                cv2.imshow('Warped', np.zeros((252, 252)))
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            print("FPS: {}".format(time.time() - start_time))
            start_time = time.time()
        vid.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
