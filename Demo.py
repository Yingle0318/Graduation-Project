
from pygame.constants import *
from OpenGL.GLU import *
import os
from OBJ_Loader import *
import numpy as np
import cv2
from GO import *
import part0.utils as utils

global parameter
parameter = [0,0,0,0,0,0]
# cv2.namedWindow('img')
# KEY  = False
# KEY_2 = False
#
# def update(x):
#     global KEY
#     if x == 1:
#         #do_something()
#         KEY = True
#         cv2.setTrackbarPos('button', 'img', 1)
#
#     if x == 0:
#         KEY = False
#         cv2.setTrackbarPos('button', 'img', 0)
#
# def update2(x):
#     global KEY_2
#     if x == 1:
#         # do_something()
#         KEY_2 = True
#         cv2.setTrackbarPos('button', 'img', 1)
#
#     if x == 0:
#         KEY_2 = False
#         cv2.setTrackbarPos('button', 'img', 0)




def control_mouth(parameter):
    mouth_index = [47, 119, 123, 127, 59, 121, 125, 129]
    Multi = [0,-0.88,0]
    for index in mouth_index :
        # plusIndex = [0, -2.2, 0]
        modelList[0].updateVertices(Multi, index, parameter)
def control_left_eyeBrow(parameter):
    left_eyeBrow_index = [112, 108, 7, 100]
    Multi = [0,1.02 /1.2,0]
    for index in left_eyeBrow_index:
        # plusIndex = [0, -2.2, 0]
        modelList[0].updateVertices(Multi, index, parameter)
def control_right_eyeBrow(parameter):
    right_eyeBrow_index = [115,111,102,104]
    Multi = [0, 1.2/1.2, 0]
    for index in right_eyeBrow_index:
        # plusIndex = [0, -2.2, 0]
        modelList[0].updateVertices(Multi, index, parameter)
def control_left_eye(parameter):
    left_eye_index = [89, 88, 91, 90]
    Multi = [0,-0.552 /4.5,0]
    for i,index in enumerate(left_eye_index) :

        if i <2:
            modelList[0].updateVertices(Multi, index, parameter)
        else:
            Multi = [0, 0.552 /4.5, 0]
            modelList[0].updateVertices(Multi, index, parameter)
def control_right_eye(parameter):
    right_eye_index = [85,84,86,87]
    Multi = [0,-0.545/6,0]
    for i,index in enumerate(right_eye_index) :

        if i <2:
            modelList[0].updateVertices(Multi, index, parameter)
        else:
            Multi = [0,0.545/6,0]

            modelList[0].updateVertices(Multi, index, parameter)



if __name__ == "__main__":
    #cap = cv2.VideoCapture('Trump.mp4')
    cap = cv2.VideoCapture(0)

    os.chdir('D:\\A_study\\projects\Graduation Project\Bruno\\newModel\Bruno_demo\Skull Model')
    file_list = os.listdir(r"D:\A_study\projects\Graduation Project\Bruno\newModel\Bruno_demo\Skull Model")
    # SCREEN SETTINGS
    pygame.init()
    display = (500, 500)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    COLOR_INACTIVE = (100, 80, 255)
    COLOR_ACTIVE = (100, 200, 255)
    COLOR_LIST_INACTIVE = (255, 100, 100)
    COLOR_LIST_ACTIVE = (255, 150, 150)
    pygame.display.set_caption('TMD Skull Model DEMO')

    modelList = []
    j = 0
    for i in range(0, len(file_list)):
        if file_list[i] == "original.mtl":
            continue
        else:
            modelList.append(OBJ(file_list[i], swapyz=False))
            j += 1

    modelIndex = 0
    rx, ry = (0, 0)
    tx, ty = (0, 0)
    zpos = 5
    rotate = move = False


    count = 0
    cv2.createTrackbar('Candide3', 'img', 0, 1, update)
    cv2.createTrackbar('BOX', 'img', 0, 1, update2)
    while True:
        # get a frame
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1, dst=None)
        # show a frame
        # cv2.imshow("capture", frame)
        paras = [0,0,0,0,0,0]
        if count > 5:
            paras = One_Picture(frame)
            paras = np.abs(paras)

            #paras = utils.normalization(paras)
            print("paras")
            print("Mouth            ", paras[0])
            print("Left_eyeBrow         ", paras[1])
            print("right_eyeBrow        ", paras[2])
            print("lefy_eye             ", paras[3])
            print("right_eye            ", paras[4])
            print("????",paras[5])
            # if max(paras) < 0.3:
            #     paras = np.zeros_like(paras)
            # if paras.all() == 0:
            #     continue
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        else:
            count += 1
            continue

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
        pre_para = parameter
        control_mouth(-pre_para[0])
        control_left_eyeBrow(-pre_para[2])
        control_right_eyeBrow(-pre_para[1])
        control_left_eye(-pre_para[4])
        control_right_eye(-pre_para[3])

        cur_para = paras
        control_mouth(cur_para[0])
        control_left_eyeBrow(cur_para[2])
        control_right_eyeBrow(cur_para[1])
        control_left_eye(cur_para[4])
        control_right_eye(cur_para[3])
        parameter = cur_para



        #cur_para = np.random.uniform()
        #control_left_eyeBrow(cur_para)
        #parameter = cur_para
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluPerspective(45, (display[0] / display[1]), 1, 100)
        glTranslatef(0.0, 0.0, -15)
        glRotatef(180, 0, 1, 0)
        glRotatef(90, 0, 1, 0)

        # RENDER OBJECT
        glTranslate(tx / 20., ty / 20., zpos - 5)
        glRotate(rx, 0, 1, 0)
        # glRotate(ry, 0, 1, 0)
        glRotate(ry, 0, 0, 1)
        # glLoadIdentity()
        #\glRotatef(90, 1, 0, 0)

        glCallList(modelList[modelIndex].gl_list)
        # glCallList(pig.gl_list)

        pygame.display.flip()
        # print(pig.vertices[pig.index[47]])
    cap.release()
    cv2.destroyAllWindows()