import numpy as np
import model
import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
#from OpenGL.GLU import *

####################################################################################################################
#       Load Candide-3 Model
#
candide3 = model.Candide3()
VERTEX_LIST = candide3.vertexs * 0.8
FACE_LIST = candide3.faces
AUS = candide3.aus
AUV0 = AUS[0:10]
AUV11 = AUS[10:22]
AUV6 = AUS[76:88]

####################################################################################################################
#  key_ control
count_A = 0

####################################################################################################################
def normalization(data):
    _range = np.max(abs(data))
    return data / _range
def key_callback(window, key, scancode, action, mods):
    global count_A
    if key==glfw.KEY_A:
        if action==glfw.PRESS and count_A == 0:
            count_A +=1
            print(AUV11)
            for auv in AUV11:

                VERTEX_LIST[int(auv[0])] = (-1)*VERTEX_LIST[int(auv[0])]*np.array(auv[1:])+VERTEX_LIST[int(auv[0])]
            print(VERTEX_LIST.shape)
        elif action==glfw.RELEASE:
            print('release a')
        elif action==glfw.REPEAT:
            print('repeat a')


def render(T,VERTEX_LIST,FACE_LIST):


    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()
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
        glVertex3fv(VERTEX_LIST[int(face[0])])
        glVertex3fv(VERTEX_LIST[int(face[1])])
        glVertex3fv(VERTEX_LIST[int(face[2])])

        glEnd()

def main():
    #####################################################################################################################

    if not glfw.init():
        return
    window = glfw.create_window(1024, 1024, "Candide_wfm", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()


        id = np.identity(3)
        render(id,VERTEX_LIST,FACE_LIST)

        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
