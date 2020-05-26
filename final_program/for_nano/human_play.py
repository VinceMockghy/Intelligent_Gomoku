# -*- coding: utf-8 -*-
"""
human VS AI models
Input your move in the format: 2,3

@author: Junxiao Song
"""

from __future__ import print_function
import pickle
import tensorflow as tf
from game import Board, Game
from mcts_pure import MCTSPlayer as MCTS_Pure
from mcts_alphaZero import MCTSPlayer
# from policy_value_net_numpy import PolicyValueNetNumpy
# from policy_value_net import PolicyValueNet  # Theano and Lasagne
# from policy_value_net_pytorch import PolicyValueNet  # Pytorch
from policy_value_net_tensorflow import PolicyValueNet # Tensorflow
# from policy_value_net_keras import PolicyValueNet  # Keras
# from _search import getpoint
import cv2
import time
import numpy as np
from periphery import GPIO


point = []
count = 9
k = 60
for i in range(count):
    t = 60
    for j in range(count):
        point.append([k, t, 0])
        t = t + 60
    k = k + 60

class Human(object):
    """
    human player
    """

    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
#         move = getpoint()

        try:
            #在这里调用摄像头拍照！读取棋子位置，需要新函数返回落点move（x*9+y）
            time.sleep(1)
#             fflag=1
            move = getpoint()
#             print(move)
            
#             try:
#                 move=getpoint()
#                 fflag=1
#             except BaseException as e:
#                 fflag=0
#                 print("again")

#             location = input("Your move: ")
#             if isinstance(location, str):  # for python3
#                 location = [int(n, 10) for n in location.split(",")]
#             move = board.location_to_move(location)
            
        except Exception as e:
            move = -1
        if move == -1 or move not in board.availables:
            print("invalid move")
            move = self.get_action(board)
        return move

    def __str__(self):
        return "Human {}".format(self.player)


def run():
    n = 5
    width, height = 9, 9
#     model_file = 'best_policy_8_8_5.model'
    model_file = './model/best_policy.model'
#     model_file = tf.train.import_meta_graph('./model/current_policy.model')
#     model_file = './model/froze_885.pb'
    try:
        board = Board(width=width, height=height, n_in_row=n)
        game = Game(board)

        # ############### human VS AI ###################
        # load the trained policy_value_net in either Theano/Lasagne, PyTorch or TensorFlow
        
        
#         best_policy = PolicyValueNetNumpy(width, height,model_file)

        best_policy = PolicyValueNet(width, height, model_file = model_file)
        mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=200)

        # load the provided model (trained in Theano/Lasagne) into a MCTS player written in pure numpy
#         try:
#             policy_param = pickle.load(open(model_file, 'rb'))
#         except:
#             policy_param = pickle.load(open(model_file, 'rb'),
#                                        encoding='bytes')  # To support python3
#         best_policy = PolicyValueNetNumpy(width, height, policy_param)
#         mcts_player = MCTSPlayer(best_policy.policy_value_fn,
#                                  c_puct=5,
#                                  n_playout=200)  # set larger n_playout for better performance

        # uncomment the following line to play with pure MCTS (it's much weaker even with a larger n_playout)
#         mcts_player = MCTS_Pure(c_puct=5, n_playout=1000)

        # human player, input your move in the format: 2,3
        human = Human()
        # set start_player=0 for human first
        game.start_play(human, mcts_player, start_player=0, is_shown=1)
    except KeyboardInterrupt:
        print('\n\rquit')

def getpoint():
    maxHeight = 480
    maxWidth = 640
    capture = cv2.VideoCapture(0)
    capture.set(3,maxWidth)
    capture.set(4,maxHeight)
    gpio_get = GPIO(38,"in")
    while True:
        ret, image = capture.read()
        image = cv2.resize(image, (640, 480), interpolation=cv2.INTER_CUBIC)
        image=cv2.flip(image,1)
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', image)
#         time_in+=1
        k=cv2.waitKey(1)
        value = gpio_get.read()
        if value == False:
            break
    gpio_get.close()
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
    print("1")
    kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 5))
    cannyimg = cv2.morphologyEx(cannyimg, cv2.MORPH_CLOSE, kernelX)

    circles = cv2.HoughCircles(cannyimg, cv2.HOUGH_GRADIENT, 1, 20, param1=100, param2=5, minRadius=2, maxRadius=13)

    circles = np.uint16(np.around(circles))
    print("2")

    center = [[circles[0][0][0], circles[0][0][1]], [circles[0][1][0], circles[0][1][1]], [circles[0][2][0], circles[0][2][1]], [circles[0][3][0],circles[0][3][1]]]
    print("3")
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
    print("4")

    # original pts
    pts_o = np.float32([center[0], center[1], center[2], center[3]]) # 这四个点为原始图片上数独的位置
    pts_d = np.float32([[0, 0], [600, 0], [0, 600], [600, 600]]) # 这是变换之后的图上四个点的位置
    print("5")
    # get transform matrix
    M = cv2.getPerspectiveTransform(pts_o, pts_d)
    print("6")
    # apply transformation
    dst = cv2.warpPerspective(image, M, (600, 600)) # 最后一参数是输出dst的尺寸。可以和原来图片尺寸不一致。按需求来确定
    print("7")
    image = dst
#     cv2.imshow("img",image)
#     cv2.waitKey(0)


#     low_color2 = np.array([80, 20, 20])
#     up_color2 = np.array([255, 150, 80])
    low_color2 = np.array([130, 0, 0])
    up_color2 = np.array([255, 150, 100])

#     print("8")
    n = len(point)
    print(n)
    for index in range(n):
#         print("xxxxx")
        bgr = image[point[index][0],point[index][1]]
        bgr = np.array(bgr)

        if (low_color2 <= bgr).all() and (up_color2 >= bgr).all():

            if point[index][2] == 0:
                point[index][2] = 1
#                 print("xxxxxx")
                print(index,type(index))
                return index




if __name__ == '__main__':
    run()
