import pygame

from pygame.constants import *
from OpenGL.GLU import *
from OpenGL import *
from OBJ_Loader import *
import part0.model as model
import part0.utils as utils
import cv2
import numpy as np
import dlib
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import control
import time
###############################################################
####  Data preprocessing
###  important   重要
###
###  因为 opencv的y 与 candide3的 y轴方向相反
##
#print(candide3.vertexs[:,1])

cv2.namedWindow('img')
KEY = False
KEY_2 = False

def update(x):
    global KEY
    if x == 1:
        #do_something()

        KEY = True
        cv2.setTrackbarPos('button', 'img', 1)

    if x == 0:

        KEY = False
        cv2.setTrackbarPos('button', 'img', 0)

def update2(x):
    global KEY_2
    if x == 1:
        # do_something()
        KEY_2 = True
        cv2.setTrackbarPos('button', 'img', 1)

    if x == 0:
        KEY_2 = False
        cv2.setTrackbarPos('button', 'img', 0)







# global parameter
# parameter = 0
candide3=model.Candide3()
candide3.mean3D[:,1] = -1* candide3.mean3D[:,1]
######## you can changed the number of parameters
n_para = 6+6
skull_up_or_down = np.array([1,-1,1,1,1,1])
candide3.getBlendshapes()
if len(skull_up_or_down) != n_para - 6:
    print("FUUUUUUUUUK")
if len(candide3.blendshapes) != n_para - 6:
    print("FUUUUUUUUUK")

#
# 人脸检测器
detector = dlib.get_frontal_face_detector()
# 特征点检测器
predictor = dlib.shape_predictor("D:\A_study\projects\Graduation Project\shape_predictor_68_face_landmarks.dat")
################################################################

def face_detect(color_image,DrawRentangle,DrawNumbers, DrawPoints,DrawkeyPoints):
    # DrawRentangle = True
    # DrawNumbers = False
    # DrawPoints =  True
    # DrawkeyPoints = True
    #color_image = cv2.imread(file_path)
    #color_image = cv2.resize(color_image,None, fx=2, fy=2) #放大3倍
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)  # 将彩色图片转换为灰色图片，提高人脸检测的准确率
    origin_img = color_image.copy()
    # 也可以不用转换灰色图像，但是BGR要转换为RGB
    # color_image = cv2.imread(file_path, cv2.IMREAD_COLOR)
    # B, G, R = cv2.split(color_image)   # 分离三个颜色通道
    # color_image = cv2.merge([R, G, B]) # 融合三个颜色通道生成新图片

    # 检测人脸
    # The 1 in the second argument indicates that we should upsample the image 1 time.
    faces = detector(gray_image, 1)

    # 调用训练好的卷积神经网络（cnn）模型进行人脸检测
    # cnn_face_detector = dlib.cnn_face_detection_model_v1('model/mmod_human_face_detector.dat')
    # faces = cnn_face_detector(gray_image, 1)
    global KEY

    points_68_2D = []
    for face in faces:
        #print("face")
        #print(face)

        #cv2.imshow("face",face)
        #cv2.waitKey(0)
        #global KEY_2
        #if DrawRentangle:
        #global KEY_2
        if KEY_2:

            # 用矩形框住人脸
            left = face.left()
            top = face.top()
            right = face.right()
            bottom = face.bottom()
            cv2.rectangle(color_image, (left, top), (right, bottom), (0, 255, 0), 2)


            pts = np.array([[left,top],  [right, top], [right, bottom],[left , bottom]], np.int32)
            #copy_pts = pts
            pts = pts.reshape((-1, 1, 2))

            cv2.polylines(color_image, [pts], True, (0, 255, 255))


            #return left,top,right,bottom
        if DrawPoints:
        # 寻找人脸的68个标定点
            shape = predictor(color_image, face)
            # 遍历所有点，打印出其坐标，并圈出来
            for idx, pt in enumerate(shape.parts()):
                pt_pos = (pt.x, pt.y)
                points_68_2D.append(pt_pos)
                if DrawkeyPoints:
                    if idx in candide3.idxs2D:

                        cv2.circle(color_image, pt_pos, 2, (0, 255, 0), -1)
                    else:
                        cv2.circle(color_image, pt_pos, 2, (0, 255, 255), -1)
                else:
                    cv2.circle(color_image, pt_pos, 2, (0, 255, 255), -1)

                if DrawNumbers:# 利用cv2.putText输出1-68
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(color_image, str(idx), pt_pos, font, 0.3, (255, 0, 0), 1, cv2.LINE_AA)


                # 位置，字体，大小，颜色，字体厚度
        #print(points_2D)


    return np.array(points_68_2D)
################################################################
###
##
#      Drawing!
#

def drawProjected2D(img,projected2D):
    # print(projected2D.shape)
    # print(projected2D.T)
    pts = projected2D.T
    # draw points
    for point in pts:


        cv2.circle(img, (int(point[0]), int(point[1])), 2, (0,0,255)) # red

    # draw mesh
    for tri in candide3.faces:
        #print(tri)
        p1 = pts[int(tri[0])].astype(int)
        p2 = pts[int(tri[1])].astype(int)
        p3 = pts[int(tri[2])].astype(int)

        p1 = (p1[0],p1[1])
        p2 = (p2[0], p2[1])
        p3 = (p3[0], p3[1])
        cv2.line(img,p1,p2,(0,0,255))
        cv2.line(img, p2, p3, (0, 0, 255))
        cv2.line(img, p1, p3, (0, 0, 255))
    #cv2.imshow('img', img)


def drawCandide(vertices):

    #DrawAllblendshapes = True
    Drawkey_index = False

    fig = plt.figure()
    ax = Axes3D(fig)
    #vertices = candide3.vertexs.copy()
    key_index = candide3.idxs3D


    for i , vertex in enumerate(vertices):
        if Drawkey_index:
            if i in key_index:
                x = vertices[i][0]
                y = vertices[i][1]
                z = vertices[i][2]
                ax.scatter(x, y, z, color='r', label='key',marker="*")  # 绘制散点图
                ax.text(x,y,z,s = str(i))
        else:
            x = vertices[i][0]
            y = vertices[i][1]
            z = vertices[i][2]
            ax.scatter(x, y, z, color='b', label='non-key', )


            #ax.scatter(x2,y2,z2, color='g',label='others')

    faces =  candide3.faces

    for face in faces:

        p1 = vertices[int(face[0])]
        p2 = vertices[int(face[1])]

        p3 = vertices[int(face[2])]

        x = [p1[0], p2[0]]
        y = [p1[1], p2[1]]
        z = [p1[2], p2[2]]
        ax.plot(x, y, z, c='black')
        x = [p1[0], p3[0]]
        y = [p1[1],  p3[1]]
        z = [p1[2], p3[2]]
        ax.plot(x, y, z, c='black')
        x = [ p2[0], p3[0]]
        y = [ p2[1], p3[1]]
        z = [ p2[2], p3[2]]
        ax.plot(x, y, z, c='black')
        #verts = [list(zip(x, y, z))]
        #ax.add_collection3d(Poly3DCollection(verts))

    plt.show()
################################################################
###############################################
#
#               FITTING ALGORITHMS
#
#
def fun(dlib46,candide46,mean3D,blendshapes,parameters):

    #start_fun = time.time()
    s = parameters[0]
    r = parameters[1:4]
    t = parameters[4:6]
    w = parameters[6:]
    #w = np.ones(10)
    #up_or_down_or_down = np.array([-1,-1,-1,1,-1,1,1,1,1,1])
    shape3D = mean3D.copy()
    #exaggerate = 1
    for i, auvs in enumerate (blendshapes[:(n_para - 6)]):
    #for i, auvs in enumerate(blendshapes):
        for auv in auvs:
            #print(auv[0])
            #p
            shape3D[int(auv[0])] =skull_up_or_down[i]* w[i]*auv[1:]*mean3D[int(auv[0])]+ shape3D[int(auv[0])]
        #drawCandide(shape3D)
    # print("r:   ",r*180)

    R = cv2.Rodrigues(r)[0]
    # print("R:   ",R)
    P = R[:2]
    projected = s * np.dot(P, shape3D.T)+ t.T[:, np.newaxis]
   # print("?")
    #print(projected.shape)

    projected_46 = []
    for idx3D in candide3.idxs3D:
        projected_46.append(projected.T[idx3D])
    projected_46 = np.array(projected_46)
    f_X = projected_46 - dlib46
    f_X =f_X.flatten()


 #   end_fun = time.time()
#    print("fun time  ", end_fun - start_fun)
    return f_X
def diff_c(dlib46,stepSize):
    #start_diffc = time.time()

    jacobian = np.zeros((92,n_para))
    for i  in range(n_para):
        step = np.zeros(n_para)
        step[i] += stepSize
        jacobian[:,i] = (fun(dlib46,None,candide3.mean3D,candide3.blendshapes,candide3.parameters[:n_para] + step)
                         - fun(dlib46,None,candide3.mean3D,candide3.blendshapes,candide3.parameters[:n_para] - step)) / ( 2 * stepSize)
    #end_diffc = time.time()
    #print("diffc")
    #print(end_diffc-start_diffc)
    return jacobian

def GN(dlib_46,project_46,mean3D,blendshapes,parameters):

    stop = 1
    index_stop = 0
    x  = candide3.parameters[:n_para]

    draw_i = np.arange(100)
    draw_x = np.zeros(100)
    iternums = 100
    for i in range(iternums):

        f_x = fun(dlib_46, None, candide3.mean3D, candide3.blendshapes, x)
        old_cost = np.dot(f_x.T, f_x)
        draw_x[i] = old_cost
        J = diff_c(dlib_46, 0.001)
        H = np.dot(J.T, J)
        H_inv = np.linalg.pinv(H)
        g = np.dot(-J.T, f_x)

        deltaX = np.dot(H_inv, g)

        x = x + deltaX
        newf_x = fun(dlib_46, None, candide3.mean3D, candide3.blendshapes, x)
        new_cost = np.dot(newf_x.T,newf_x)

        #print("i {} / {}  cost   {}  \n  x {}".format(i + 1, iternums, old_cost, x))
        if abs(old_cost - new_cost) < stop:

            #index_stop = i
            #print("index stop")
            #print(index_stop)
            break


    # draw cost function
    # plt.plot(draw_i[:index_stop],draw_x[:index_stop])
    # plt.show()
    return x
##
###########################################################


def One_Picture(img):
    global KEY_2
    #start = time.time()
    dlib_68 = face_detect(img,True,False,True,True)

    if dlib_68 != []:
        #print(dlib_68)
        candide3.initParmeters(dlib_68)


        dlib_46 = []
        for idx2D in candide3.idxs2D:
            dlib_46.append(dlib_68[idx2D])
        dlib_46 = np.array(dlib_46)

        # candi_46 = []
        # for idx3D in candide3.idxs3D:
        #     candi_46.append(candide3.mean3D[idx3D])
        # candi_46 = np.array(candi_46)
        #startGN = time.time()
        x = GN(dlib_46, None, None, None, None)
        r = x[1:4]
        text = " 1: "+str(round(r[0],3))+ " 2: "+str(round(r[1],3)) + " 3: "+str(round(r[2],3))
        cv2.putText(img, text, (30, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
        #cv2.putText(img, text, (30, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
        if r [1] < - 0.4:
            x[6+4] = 0
        if r[1] > 0.4:
            x[6+ 3] = 0
        #print("parametes !!!!")
        #print(x)
        # endGN = time.time()
        # print("GN ",endGN-startGN)
        candide3.parameters = x
        #[print(w) for w in utils.normalization(x[6:])]


        projected = candide3.projected()
        global KEY
        print("Fucking Key", KEY)
        if KEY:
            print("key")
            print(KEY)
            drawProjected2D(img, projected)

        # end = time.time()
        # print("One pirture")
        # print(end - start)
        #control.control_candide3(x)

        cv2.imshow('img', img)
        return x[6:]
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    else:
        cv2.imshow('img', img)
        return np.zeros_like(candide3.parameters[6:])
def main():
    ### One picture version####
    #

    # img = cv2.imread("pictures/Graduation Project1.jpg")
    # para = One_Picture(img)
    # cv2.imshow('img',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    ########################################################
    ## video  version##
    #

    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture('zoom.mp4')
    #global parameter
    global parameter
    count = 0
    #################################
    ### load video
    ##
    #

    #cap = cv2.VideoCapture('Trump.mp4')
    cv2.createTrackbar('Candide3', 'img', 0, 1, update)
    cv2.createTrackbar('BOX', 'img', 0, 1, update2)
    while (1):

        # get a frame

        ret, frame = cap.read()

        frame = cv2.flip(frame,1,dst=None)


        # show a frame
        #cv2.imshow("capture", frame)
        if count >5:
            paras = One_Picture(frame)
            print("paras")
            print("Mouth            ", paras[0])
            print("Left_eyeBrow         ", paras[1])
            print("right_eyeBrow        ", paras[2])
            print("lefy_eye             ", paras[3])
            print("right_eye            ", paras[4])
            print("????", paras[5])
            #print(paras)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            count += 1


    cap.release()
    cv2.destroyAllWindows()
    ##############################################################
if __name__ == "__main__":

    main()




