import pygame
from OpenGL.GL import *
import numpy as np

def MTL(filename):
    filename = filename
    contents = {}
    mtl = None
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError("mtl file doesn't start with newmtl stmt")
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            mtl[values[0]] = values[1]
            surf = pygame.image.load(mtl['map_Kd'])
            print(surf)
            image = pygame.image.tostring(surf, 'RGBA', 1)
            ix, iy = surf.get_rect().size
            texid = mtl['texture_Kd'] = glGenTextures(1)
            # Set the texture wrapping parameters
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            # Set texture filtering parameters
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        else:
            mtl[values[0]] = list(map(float, values[1:]))
    return contents


class OBJ:
    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.index = []
        self.name = filename
        material = None
        counter = -1
        splitCounter = 0
        stopCondition = 0
        bonesNumber = -1
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'o':
                bonesNumber += 1
                counter += 1
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
                self.index.append(splitCounter)
                splitCounter += 1
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = MTL(values[1])
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))
            stopCondition += 1
        self.verticesMatrix = np.asarray(self.vertices)
        #print(self.index)
        #self.printInfo()
        #print(min(self.vertices))
        #print(self.vertices.index(min(self.vertices)))
        #self.printInfo()
        #print(self.index)
        #print(len(self.index))
        #self.saveVertices()
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        #glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for face in self.faces:
            vertices, normals, texture_coords, material = face

            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # just use diffuse colour
                glColor(*mtl['Kd'])

            #glColor3f(1.0, 0.0, 0.0)
            glBegin(GL_POLYGON)
            #glBegin(GL_POINTS)
            #glBegin(GL_TRIANGLES)
            #glBegin(GL_LINES)
            #glColor3f(1.0, 1.0, 1.0)
            #print(self.vertices[114])
            #print(self.vertices[115])
            #glVertex3fv(self.vertices[115])
            #glEnd()
            #glBegin(GL_LINES)
            #glPointSize(5)
            for i in range(len(vertices)):
                #print(j)
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                    #glPointSize(1)
                glVertex3fv(self.vertices[vertices[i] - 1])
                #print(self.vertices[30])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()

    def saveVertices(self):
        npArray = np.asarray(self.vertices)
        np.save(self.name + ".npy", npArray)

    def drawModel(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for face in self.faces:
            vertices, normals, texture_coords, material = face

            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # just use diffuse colour
                glColor(*mtl['Kd'])

            # glColor3f(1.0, 0.0, 0.0)
            glBegin(GL_POLYGON)
            #glBegin(GL_POINTS)
            #glBegin(GL_TRIANGLES)
            #glBegin(GL_LINES)
            # glColor3f(1.0, 1.0, 1.0)
            # print(self.vertices[114])
            # print(self.vertices[115])
            # glVertex3fv(self.vertices[115])
            # glEnd()
            # glBegin(GL_LINES)
            # glPointSize(5)
            for i in range(len(vertices)):
                # print(j)
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                    # glPointSize(1)
                glVertex3fv(self.vertices[vertices[i] - 1])
                #print(self.vertices[30])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()

    def updateVertices(self, locationArray, index,factor):
        #print("BEFORE -->" + str(self.vertices[index]))

        #make d_vertices to draw

        self.vertices[index][0] += (locationArray[0] * factor)
        self.vertices[index][1] += (locationArray[1] * factor)
        self.vertices[index][2] += (locationArray[2] * factor)

        # print("AFTER -->" + str(self.vertices[index]))
        self.drawModel()