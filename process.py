import cv2
import numpy as np

contour = None

def getCoord(c):  # takes the sudoku contour and returns the end points of the sudoku
    epsilon = 0.025 * cv2.arcLength(c, True)
    c = cv2.approxPolyDP(c, epsilon, True)
    if len(c) > 3:
        # Gets the 4 corners of the object (assume it's a square)
        topLeft = tuple(min(c, key=lambda x: x[0, 0] + x[0, 1])[0])
        bottomRight = tuple(max(c, key=lambda x: x[0, 0] + x[0, 1])[0])
        topRight = tuple(max(c, key=lambda x: x[0, 0] - x[0, 1])[0])
        bottomLeft = tuple(min(c, key=lambda x: x[0, 0] - x[0, 1])[0])
        coord = (topLeft, topRight, bottomLeft, bottomRight)
        return coord


def changePerspective(image, c):  # changes the perspective
    # x, y, w, h = cv2.boundingRect(c)
    # if w > h:
    #     h = w
    # else:
    #     w = h
    h = w = 252
    pts1 = np.float32(getCoord(c))
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    res = cv2.warpPerspective(image, matrix, (w, h))
    return res


def processImg(img):
    global contour
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 10)
    threshInv = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 10)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    try:
        sudokuContour = sorted(contours, key=cv2.contourArea, reverse=True)[1]
        contour = sudokuContour
        warped = changePerspective(threshInv, sudokuContour)
        return warped
    except:
        print('Sudoku not found')

    # cv2.imshow("Image", img)
    # cv2.imshow("Warped", warped)
    # cv2.imshow("Gray", gray)
    # cv2.imshow("Thresh", threshInv)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def removeGrid(image):
    lines = cv2.HoughLinesP(image, 1, np.pi / 180, 90, minLineLength=100, maxLineGap=50)
    try:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), 0, 5)
    except:
        print('Lines not found')
    # w = image.shape[1]
    # h = image.shape[0]
    # sqr = w // 9
    # for i in range(0, w+1, sqr):
    #     cv2.line(image, (0,i), (w,i), 0, 15)
    #     cv2.line(image, (i, 0), (i, h), 0, 15)

    return image


def putNum(img, mat, pos):
    image = np.ones_like(img)
    image = image * 255

    for i in range(0, 9):
        for j in range(0, 9):
                x, y = pos[j][i]['pos']
                cv2.putText(image, str(mat[i][j]), (x + 7, y + 21), cv2.FONT_HERSHEY_PLAIN, 1.5, 0, 1)
    return image


def reverseWarp(warped, img):
    global contour
    h = w = 252
    pts1 = np.float32(getCoord(contour))
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts2, pts1)
    print('reverse warp')
    res = cv2.warpPerspective(warped, matrix, (img.shape[1], img.shape[0]),borderValue=(255,255,255))
    res = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
    img1 = cv2.bitwise_and(img, res)
    return img1