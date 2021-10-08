from OpenGL.GL import *
from OpenGL.GLUT import *
import part0.model as model
import  numpy as np
import part0.utils as utils
import cv2
candide3 = model.Candide3()
candide3.getBlendshapes()
VERTEX_LIST = candide3.mean3D
# ones = np.ones((1,VERTEX_LIST.shape[0]))
# VERTEX_LIST = np.column_stack((VERTEX_LIST,ones.T))#Homogeneous
VERTEX_LIST = utils.Homogeneous(VERTEX_LIST)
mean3Dface =VERTEX_LIST.copy()
FACE_LIST = candide3.faces

M = np.identity(4)
exaggerate = 0.5
upper_or_down = np.array([-1, -1, -1, 1, -1, 1, 1, 1, 1, 1])
def expression(weights):
    for i,auvs in  enumerate(candide3.blendshapes[:10]):
        for auv in auvs:
            VERTEX_LIST[int(auv[0])][:-1] = weights[i] * VERTEX_LIST[int(auv[0])][:-1] * np.array(auv[1:]) + VERTEX_LIST[int(auv[0])][:-1]
def render():
    glClear(GL_COLOR_BUFFER_BIT)

    #
    # glBegin(GL_POINTS)
    # for v in VERTEX_LIST:
    #     glColor3ub(255, 0,0)
    #     glVertex3fv(v)
    #
    #
    # glEnd()

    for face in FACE_LIST:
        glBegin(GL_LINE_LOOP)
        #glBegin(GL_POINTS)
        glColor3ub(255,255 ,255 )

        glVertex3fv((M @VERTEX_LIST[int(face[0])])[:-1])
        glVertex3fv((M @VERTEX_LIST[int(face[1])])[:-1])
        glVertex3fv((M @VERTEX_LIST[int(face[2])])[:-1])

        glEnd()
    glFlush()
    glutPostRedisplay()
    return
def control_candide3(parameters):
    #s = parameters[0]
    r = parameters[1:4]
    #t = parameters[4:6]
    w = parameters[6:]

    R = cv2.Rodrigues(r)[0]
    global M

    R = np.insert(R,3,values= np.zeros(3),axis=0)
    R = np.insert(R,3,values=np.array([0,0,0,1]),axis=1)

    #R[2] = np.array([0,0,1,0])
    print(R)

    M = R


    expression(utils.normalization(w))

    glutInit()  # 1. 初始化glut库
    glutInitWindowSize(600, 600)
    glutCreateWindow('Candide3 Model')  # 2. 创建glut窗口
    glutDisplayFunc(render)  # 3. 注册回调函数draw()

    glutAttachMenu(GLUT_RIGHT_BUTTON)
    glutMainLoop()  # 4. 进入glut主循环