import sys, pygame
from pygame.constants import *
from OpenGL.GLU import *
import os
from OBJ_Loader import *

if __name__ == "__main__":
    lightpos = [100., 10., 100., 10.]

    # SCREEN SETTINGS
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    COLOR_INACTIVE = (100, 80, 255)
    COLOR_ACTIVE = (100, 200, 255)
    COLOR_LIST_INACTIVE = (255, 100, 100)
    COLOR_LIST_ACTIVE = (255, 150, 150)

    # GRAPHIC PROPERTIES
    glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, lightpos)
    glEnable(GL_LIGHT0)
    #glEnable(GL_LIGHTING)
    glEnable(GL_FRAMEBUFFER_SRGB)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_BLEND)
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(2.0, 2.0)
    glShadeModel(GL_SMOOTH)
    #os.chdir('C:\\Users\\Bruno\\Desktop\\Pig Model\\Action Units')
    file_list = os.listdir(r"C:\\Users\\Bruno\\Desktop\\Pig Model\\Action Units")
    pigList = []
    j = 0
    for i in range(0, len(file_list)):
        if file_list[i] == "original.mtl":
            continue
        else:
            pigList.append(OBJ(file_list[i], swapyz=False))
            print(pigList[j].name)
            j += 1
    #pig = OBJ("eyesClosed.obj", swapyz=False)
    clock = pygame.time.Clock()
    glMatrixMode(GL_PROJECTION)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    pigIndex = 0
    rx, ry = (0, 0)
    tx, ty = (0, 0)
    zpos = 5
    rotate = move = False
    while 1:
        clock.tick(30)
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                sys.exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 4:
                    zpos = max(1, zpos + 1)
                elif e.button == 5:
                    zpos -= 1
                elif e.button == 1:
                    rotate = True
                elif e.button == 2:
                    move = True
                elif e.button == 3:
                    if pigIndex < 8:
                        pigIndex += 1
                    else:
                        pigIndex = 0
            elif e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    rotate = False
                elif e.button == 2:
                    move = False
            elif e.type == MOUSEMOTION:
                i, j = e.rel
                if rotate:
                    rx += i
                    ry -= j
                if move:
                    tx -= i
                    ty += j

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluPerspective(45, (display[0] / display[1]), 1, 100)
        glTranslatef(0.0, 0.0, -10)
        #glTranslatef(0.0, -0.2, 0.0)
        glRotatef(180, 0, 1, 0)

        # RENDER OBJECT
        glTranslate(tx / 20., ty / 20., - zpos)
        glRotate(ry, 1, 0, 0)
        glRotate(rx, 0, 1, 0)

        #glLoadIdentity()
        #glRotatef(90, 1, 0, 0)
        glCallList(pigList[pigIndex].gl_list)

        pygame.display.flip()
