# encoding：utf-8
# 绿色检测

import cv2
import numpy as np




def getpoint():
    capture = cv2.VideoCapture(1)
    while True:
        ret, image = capture.read()
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', image)
        k=cv2.waitKey(1)
        if k == ord('q'):
            break
        # elif k == ord('s'):
        #     cv2.imwrite('./example.jpg',frame)
        #     print("done!")
    # 颜色范围
    low_color = np.array([35, 43, 46])
    up_color = np.array([77, 255, 255])

    # 图像处理

    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    # 颜色过滤
    mask = cv2.inRange(hsv, low_color, up_color)
    # 边缘检测
    cannyimg = cv2.Canny(mask,10,200)

#     cv2.imshow("img",cannyimg)
#     cv2.waitKey(0)

    # 闭运算
    kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 5))
    cannyimg = cv2.morphologyEx(cannyimg, cv2.MORPH_CLOSE, kernelX)

    circles = cv2.HoughCircles(cannyimg, cv2.HOUGH_GRADIENT, 1, 20, param1=100, param2=5, minRadius=2, maxRadius=13)

    circles = np.uint16(np.around(circles))


    center = [[circles[0][0][0], circles[0][0][1]], [circles[0][1][0], circles[0][1][1]], [circles[0][2][0], circles[0][2][1]], [circles[0][3][0],circles[0][3][1]]]

    n = len(center)
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n-i-1):
            if center[j][0] > center[j+1][0] :
                center[j], center[j+1] = center[j+1], center[j]
    if center[0][1] > center[1][1]:
        center[0], center[1] = center[1], center[0]
    if center[2][1] > center[3][1]:
        center[2], center[3] = center[3], center[2]
    center[1], center[2] = center[2], center[1]


    # original pts
    pts_o = np.float32([center[0], center[1], center[2], center[3]]) # 这四个点为原始图片上数独的位置
    pts_d = np.float32([[0, 0], [600, 0], [0, 600], [600, 600]]) # 这是变换之后的图上四个点的位置

    # get transform matrix
    M = cv2.getPerspectiveTransform(pts_o, pts_d)
    # apply transformation
    dst = cv2.warpPerspective(image, M, (600, 600)) # 最后一参数是输出dst的尺寸。可以和原来图片尺寸不一致。按需求来确定

    image = dst
#     cv2.imshow("img",image)
#     cv2.waitKey(0)


    low_color = np.array([80, 20, 20])
    up_color = np.array([255, 150, 80])


    n = len(point)
    for i in range(n):
        bgr = image[point[i][0],point[i][1]]
        bgr = np.array(bgr)

        if (low_color <= bgr).all() and (up_color >= bgr).all():

            if point[i][2] == 0:

                point[i][2] = 1
                return i





if __name__ == '__main__':

    point = []
    count = 9
    k = 60
    for i in range(count):
        t = 60
        for j in range(count):
            point.append([k, t, 0])
            t = t + 60
        k = k + 60
    # print(point)

    # print(n)
    while True:
        p=getpoint()
        print(p)