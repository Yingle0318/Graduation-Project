import sys, pygame
import time
import copy
import sys
from pygame.constants import *
from OpenGL.GLU import *
import os
from OBJ_Loader import *
import numpy as np




global parameter
parameter = [0,0,0,0,0]
actionUnitsDifference = []
changedModels = []


def compareModels(A, B):
    changeCounter = 0
    changeArray = []
    for i in range(0, len(A)):
        makeChange = [0.0, 0.0, 0.0, 0.0]
        if A[i][0] != B[i][0] or A[i][1] != B[i][1] or A[i][2] != B[i][2]:
            changeCounter += 1
            makeChange[3] = (float(i))
            if A[i][0] != B[i][0]:
                '''print("VERTEX " + str(i) + " IN X: ")
                print(A[i][0])
                print(B[i][0])'''
                makeChange[0] = (B[i][0] - A[i][0])

            if A[i][1] != B[i][1]:
                '''print("VERTEX " + str(i) + " IN Y: ")
                print(A[i][1])
                print(B[i][1])'''
                makeChange[1] = (B[i][1] - A[i][1])

            if A[i][2] != B[i][2]:
                '''print("VERTEX " + str(i) + " IN Z: ")
                print(A[i][2])
                print(B[i][2])'''
                makeChange[2] = (B[i][2] - A[i][2])

            changeArray.append(makeChange)

    #print("TOTAL VERTICES THAT CHANGED --> " + str(changeCounter))
    return changeArray

def control_mouth(parameter):
    mouth_index = [47, 119, 123, 127, 59, 121, 125, 129]
    Multi = [0,-2.2,0]
    for index in mouth_index :
        # plusIndex = [0, -2.2, 0]
        modelList[0].updateVertices(Multi, index, parameter)
def control_left_eyeBrow(parameter):
    left_eyeBrow_index = [112, 108, 7, 100]
    Multi = [0,1.02,0]
    for index in left_eyeBrow_index:
        # plusIndex = [0, -2.2, 0]
        modelList[0].updateVertices(Multi, index, parameter)
def control_right_eyeBrow(parameter):
    right_eyeBrow_index = [115,111,102,104]
    Multi = [0, 1.2, 0]
    for index in right_eyeBrow_index:
        # plusIndex = [0, -2.2, 0]
        modelList[0].updateVertices(Multi, index, parameter)
def control_left_eye(parameter):
    left_eye_index = [89, 88, 91, 90]
    Multi = [0,-0.552,0]
    for i,index in enumerate(left_eye_index) :

        if i <2:
            modelList[0].updateVertices(Multi, index, parameter)
        else:
            Multi = [0, 0.552, 0]
            modelList[0].updateVertices(Multi, index, parameter)
def control_right_eye(parameter):
    right_eye_index = [85,84,86,87]
    Multi = [0,-0.545,0]
    for i,index in enumerate(right_eye_index) :

        if i <2:
            modelList[0].updateVertices(Multi, index, parameter)
        else:
            Multi = [0,0.545,0]

            modelList[0].updateVertices(Multi, index, parameter)

# def Control(parameter):
#     indexs = []
#     mouth_index = [47,119,123,127,59,121,125,129]
#
#     left_eyeBrow_index = [112,108,7,100]
#     right_eyeBrow_index = [115,111,102,104]
#     left_eye = [89,88,91,90]
#     right_eye = [85,84,86,87]
#
#     indexs.append(mouth_index)
#     indexs.append(left_eyeBrow_index)
#     indexs.append(right_eyeBrow_index)
#     indexs.append(left_eye)
#     indexs.append(right_eye)
#
#     Multi = [[0,-2.2,0],[0,1.02,0],[0,1.2,0],[0,-0.552,0],[0,-545,0]]
#
#     # MOUTH: -2.2
#     # LEFTEYEBROW: 1.02
#     # RIGHTEYEBROW: 1.2
#     # LEFTEYE: -0.552
#     # RIGHTEYE: -0.545
#     for i,au_index in enumerate(indexs):
#         print(i)
#         for index in au_index:
#             #plusIndex = [0, -2.2, 0]
#             modelList[modelIndex].updateVertices(Multi[i], index,parameter[i])
#
#     # modelList[modelIndex].updateVertices(plusIndex, 47)
#     # modelList[modelIndex].updateVertices(plusIndex, 119)
#     # modelList[modelIndex].updateVertices(plusIndex, 123)
#     # modelList[modelIndex].updateVertices(plusIndex, 127)
#     # modelList[modelIndex].updateVertices(plusIndex, 59)
#     # modelList[modelIndex].updateVertices(plusIndex, 121)
#     # modelList[modelIndex].updateVertices(plusIndex, 125)
#     # modelList[modelIndex].updateVertices(plusIndex, 129)


if __name__ == "__main__":

    # SCREEN SETTINGS
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    COLOR_INACTIVE = (100, 80, 255)
    COLOR_ACTIVE = (100, 200, 255)
    COLOR_LIST_INACTIVE = (255, 100, 100)
    COLOR_LIST_ACTIVE = (255, 150, 150)
    pygame.display.set_caption('TMD Skull Model DEMO')

    ##GRAPHIC PROPERTIES
    glEnable(GL_LIGHT0)
    # glEnable(GL_LIGHTING)
    glEnable(GL_FRAMEBUFFER_SRGB)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_BLEND)
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(2.0, 2.0)
    glShadeModel(GL_SMOOTH)
    os.chdir('D:\\A_study\\projects\Graduation Project\Bruno\\newModel\Bruno_demo\Skull Model')
    file_list = os.listdir(r"D:\A_study\projects\Graduation Project\Bruno\newModel\Bruno_demo\Skull Model")
    modelList = []
    j = 0
    for i in range(0, len(file_list)):
        if file_list[i] == "original.mtl":
            continue
        else:
            modelList.append(OBJ(file_list[i], swapyz=False))
            print(modelList[j].name)
            j += 1
    # pig = OBJ("[2] Mouth Open.obj", swapyz=False)
    # clock = pygame.time.Clock()
    # glMatrixMode(GL_PROJECTION)
    # glEnable(GL_DEPTH_TEST)
    # #glMatrixMode(GL_MODELVIEW)

    modelIndex = 0
    rx, ry = (0, 0)
    tx, ty = (0, 0)
    zpos = 5
    rotate = move = False

    '''for i in range(1, len(modelList)):
        result = compareModels(modelList[0].verticesMatrix, modelList[i].verticesMatrix)
        actionUnitsDifference.append(result)

    backup = []
    backup.append(modelList[0].vertices)

    #print(resultantMatrix)

    print(len(actionUnitsDifference))

    for j in range(0, len(actionUnitsDifference)):
        print("J --> " + str(j))
        print("LENGTH --> " + str(len(actionUnitsDifference[j])))
        for i in range(0, len(actionUnitsDifference[j])):
            modelList[0].updateVertices(actionUnitsDifference[j][i], int(actionUnitsDifference[j][i][3]))
        changedModels.append(modelList[0].vertices)
        modelList[0] = OBJ(file_list[1], swapyz=False)
        #print(len(modelList[0].vertices))'''

    '''modelsChanged = np.asarray(changedModels)
    print(actionUnitsDifference)
    unidades = np.array(actionUnitsDifference)
    # save to npy file
    np.save('modelsChanged.npy', modelsChanged)
    np.save('units.npy', unidades)'''

    '''baseModel = np.array(modelList[0].vertices)
    print(baseModel)
    print(baseModel.shape)
    print("fuck")
    np.savez("baseModel.npz", baseModel)'''

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
        #pre_para = parameter
        control_mouth(-parameter[0])
        control_left_eyeBrow(-parameter[1])
        control_right_eyeBrow(-parameter[2])
        control_left_eye(-parameter[3])
        control_right_eye(-parameter[4])

        cur_para = np.random.uniform()
        control_mouth(cur_para)
        control_left_eyeBrow(cur_para)
        control_right_eyeBrow(cur_para)
        control_left_eye(cur_para)
        control_right_eye(cur_para)
        parameter = [cur_para] *5



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


        glCallList(modelList[modelIndex].gl_list)
        # glCallList(pig.gl_list)

        pygame.display.flip()
        # print(pig.vertices[pig.index[47]])
