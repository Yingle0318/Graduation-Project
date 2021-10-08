from OpenGL.GL import *
from OpenGL.GLUT import *
import model
import  numpy as np
import  utils

candide3 = model.Candide3()
candide3.getBlendshapes()
VERTEX_LIST = candide3.mean3D
# ones = np.ones((1,VERTEX_LIST.shape[0]))
# VERTEX_LIST = np.column_stack((VERTEX_LIST,ones.T))#Homogeneous
VERTEX_LIST = utils.Homogeneous(VERTEX_LIST)
mean3Dface =VERTEX_LIST.copy()

FACE_LIST = candide3.faces
AUS = candide3.aus
AUV0 = AUS[0:10]
AUV11 = AUS[10:22]
AUV6 = AUS[76:88]
AUV5 = AUS[68:76]
th = np.radians(-60)
R = np.array([[1., 0., 0., 0.],
                  [0., np.cos(th), -np.sin(th), 0.],
                  [0., np.sin(th), np.cos(th), 0.],
                  [0., 0., 0., 1.]])
T = np.array([[1., 0., 0., .4],
              [0., 1., 0., 0.],
              [0., 0., 1., .2],
              [0., 0., 0., 1.]])
#global M
M = np.identity(4)
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
def rt_on():
    global M
    print("rt")
    M = R @ T
    glutChangeToMenuEntry(2, "RT Off", RT_OFF)
def rt_off():
    global M
    M = np.identity(4)
    glutChangeToMenuEntry(2, "RT ON", RT_ON)
def doquit():
    sys.exit(0)
    return
def au0_on():
    for auv in AUV0:
        VERTEX_LIST[int(auv[0])][:-1] =  (-1)*VERTEX_LIST[int(auv[0])][:-1] * np.array(auv[1:]) + VERTEX_LIST[int(auv[0])][:-1]
    glutChangeToMenuEntry(3, "AU0 Off", AU0_OFF)
def auo_off():
    for auv in AUV0:
        VERTEX_LIST[int(auv[0])] = mean3Dface[int(auv[0])]
    glutChangeToMenuEntry(3, "AU0 ON", AU0_ON)
def au11_on():
    print("auv11")
    for auv in AUV11:
        VERTEX_LIST[int(auv[0])][:-1] = (-1)*VERTEX_LIST[int(auv[0])][:-1] * np.array(auv[1:]) + VERTEX_LIST[int(auv[0])][:-1]
    glutChangeToMenuEntry(4, "AU11 Off", AU11_OFF)
def au11_off():
    for auv in AUV11:
        VERTEX_LIST[int(auv[0])] =mean3Dface[int(auv[0])]
    glutChangeToMenuEntry(4, "AU11_ON", AU11_ON)
def au6_on():
    right_AUV6 = []
    right_AUV6.append(AUV6[0])
    right_AUV6.append(AUV6[1])
    #right_AUV6.append(AUV6[3])
    right_AUV6.append(AUV6[4])
    #right_AUV6.append(AUV6[5])
    right_AUV6.append(AUV6[6])
    right_AUV6.append(AUV6[8])
    right_AUV6.append(AUV6[10])

    for auv in right_AUV6:
        VERTEX_LIST[int(auv[0])][:-1] = VERTEX_LIST[int(auv[0])][:-1] * np.array(auv[1:]) + VERTEX_LIST[int(auv[0])][:-1]
    glutChangeToMenuEntry(5, "AU6 Off", AU6_OFF)
def au6_off():
    for auv in AUV6:
        VERTEX_LIST[int(auv[0])] = mean3Dface[int(auv[0])]
    glutChangeToMenuEntry(5, "AU6_ON", AU6_ON)
def au5_on():
    right_AUV5 = []
    right_AUV5.append(AUV5[0])
    right_AUV5.append(AUV5[1])
    right_AUV5.append(AUV5[2])
    right_AUV5.append(AUV5[3])

    for auv in right_AUV5:
        VERTEX_LIST[int(auv[0])][:-1] = VERTEX_LIST[int(auv[0])][:-1] * np.array(auv[1:]) + VERTEX_LIST[int(auv[0])][:-1]
    glutChangeToMenuEntry(6, "AU5_OFF", AU5_OFF)
def au5_off():
    for auv in AUV5:
        VERTEX_LIST[int(auv[0])] = mean3Dface[int(auv[0])]
    glutChangeToMenuEntry(6, "AU5_ON", AU5_ON)
### menu
AU0_ON,AU0_OFF,AU11_ON,AU11_OFF,AU6_ON,AU6_OFF, RT_ON,RT_OFF,QUIT,AU5_ON,AU5_OFF= range(11)
menudict = {AU0_ON: au0_on,
            AU0_OFF: auo_off,
            AU11_ON: au11_on,
            AU11_OFF:au11_off,
            AU6_ON :au6_on,
            AU6_OFF : au6_off,
            RT_ON: rt_on,
            RT_OFF: rt_off,
            QUIT: doquit,
            AU5_ON: au5_on,
            AU5_OFF: au5_off}
def dmenu(item):
    menudict[item]() # 函数 nm
    return 0
def main():
    glutInit()  # 1. 初始化glut库
    glutInitWindowSize(600, 600)

    glutCreateWindow('ZHU YINGE TEST')  # 2. 创建glut窗口
    glutDisplayFunc(render) # 3. 注册回调函数draw()
    glutCreateMenu(dmenu)
    glutAddMenuEntry("Quit", QUIT)
    glutAddMenuEntry("RT_ON", RT_ON)
    glutAddMenuEntry("AU0_ON", AU0_ON)
    glutAddMenuEntry("AU11_ON", AU11_ON)
    glutAddMenuEntry("AU6_ON", AU6_ON)
    glutAddMenuEntry("AU5_ON",AU5_ON)
    #glutAddMenuEntry("AU5_OFF",AU5_OFF)
    glutAttachMenu(GLUT_RIGHT_BUTTON)
    glutMainLoop()  # 4. 进入glut主循环
if __name__ == "__main__":
   main()


