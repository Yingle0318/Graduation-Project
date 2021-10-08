import cv2
import  numpy as np

class Candide3:
    def __init__(self):
        self.mean3D = np.load('candide_wfm.npz')['VERTEX_LIST']
        self.faces = np.load('candide_wfm.npz')['FACE_LIST']
        self.aus = np.load('candide_wfm.npz')['ANIMATION_UNITS_LIST']

        self.aus_index = np.array([10,22,40,54,68,76,88,100,123,131,137,140,141,142,143,144,145,146,147,148,149,150,153,156,162,170,171,174,177,180,183,187,191,195,199,203,207,211,215,216,217,219,221,222,223,226,229,230,231,232,233,236,237,238,239,240,241,242,243,244,245,248,251,254,257])

        self.shape_unit = np.load("candide_wfm.npz")['SHAPE_UNIT_LIST']
        self.idxs2D = np.array([35, 31, 30, 33, 28,
                                34, 32, 36, 37, 38,
                                39, 40, 41, 42, 43,
                                44, 45, 46, 47, 17,
                                19, 21, 22, 24, 26,
                                48, 51 ,54, 57, 53,
                                49, 55, 59, 60, 62,
                                64, 66,  7,  8,  9,
                                0,  2,  4, 16, 14, 12])
        self.idxs3D = np.array([ 26,  59,   5,   6,  94,
                                 111, 112,  53,  98, 104,
                                 56, 110, 100,  23, 103,
                                 97,  20,  99,  109,  48,
                                 49,  50 , 17,  16,  15,
                                 64,   7,  31,   8,  79,
                                 80,  85,  86,  89,  87,
                                 88, 40,  65,  10,  32,
                                 62,  61,  63,  29,  28,  30])
        #self.parameters = np.zeros(6+65)
        ####
        # YOU CAN Change the number of parameters
        #
        ###
        self.parameters = np.zeros(6 + 6)
        # s r1 r2 r3 t1  t2 [w1-w11] 先弄0个


        #         self.camera_matrix=np.array([
        #     [1394.6027293299926,0,995.588675691456],
        #     [0,1394.6027293299926,599.3212928484164],
        #     [0,0,1]
        # ],dtype="double")
        #         self.distortion_coefficient = np.array([ 0.11480806073904032,-0.21946985653851792, 0.0012002116999769957,0.008564577708855225,0.11274677130853494],dtype="double")
        #

    def getBlendshapes(self):
        self.blendshapes  = []

        for i, index in  enumerate(self.aus_index):

            if i == 0:
                self.blendshapes.append(self.aus[0:index])

            else:

                front_index = self.aus_index[i-1]
                if i == 5:
                    print(front_index,index)
                self.blendshapes.append(self.aus[front_index:index])
        self.blendshapes = np.array(self.blendshapes)
        ######### for TMD blenshape
        #
        #
        mouth = self.blendshapes[1]
        left_eyeBrow = self.blendshapes[5][4:]
        right_eyeBrow = self.blendshapes[5][:4]
        left_eye = []
        left_eye.append(self.blendshapes[6][0])
        left_eye.append(self.blendshapes[6][1])
        left_eye.append(self.blendshapes[6][4])
        left_eye.append(self.blendshapes[6][6])
        left_eye.append(self.blendshapes[6][8])
        left_eye.append(self.blendshapes[6][10])
        left_eye = np.array(left_eye)
        right_eye = []
        right_eye.append(self.blendshapes[6][2])
        right_eye.append(self.blendshapes[6][3])
        right_eye.append(self.blendshapes[6][5])
        right_eye.append(self.blendshapes[6][7])
        right_eye.append(self.blendshapes[6][9])
        right_eye.append(self.blendshapes[6][11])
        right_eye = np.array(right_eye)
        #up_lip_raiser = []
        up_lid_raiser = self.blendshapes[9]
        up_lip_raiser=self.blendshapes[0]
        self.blendshapes = []

        self.blendshapes.append(mouth)
        self.blendshapes.append(left_eyeBrow)
        self.blendshapes.append(right_eyeBrow)
        self.blendshapes.append(left_eye)
        self.blendshapes.append(right_eye)
        self.blendshapes.append(up_lip_raiser)
        #self.blendshapes.append(up_lid_raiser)
        self.blendshapes = np.array(self.blendshapes)
        #print(self.blendshapes[1])

    def initParmeters(self,points_68_2D):

        points_46_3D = []
        points_46_2D = []
        for index_3D in self.idxs3D:
            points_46_3D.append(self.mean3D[index_3D])
        points_46_3D = np.array(points_46_3D)
        for index_2D in self.idxs2D:

            points_46_2D.append(points_68_2D[index_2D])
        points_46_2D = np.array(points_46_2D)


        #  (x-mean) / u
        #  标准化
        centred_3D = points_46_3D - np.mean(points_46_3D,axis=0)  # 中心化
        centred_2D = points_46_2D - np.mean(points_46_2D,axis=0)
        scale = np.linalg.norm(centred_2D) /  np.linalg.norm(centred_3D[:,:2])

        # 利用 中心点 求t
        t = np.mean(points_46_2D,axis=0) - np.mean(points_46_3D[:,:2],axis= 0)


        self.parameters[0] = scale
        self.parameters[4] = t[0]
        self.parameters[5] = t[1]

    def projected(self):
        s = self.parameters[0]
        r = self.parameters[1:4]
        t = self.parameters[4:6]
        w = self.parameters[6:]  #一共有5个 changed
        #print("??????")
        #print(w)
        #print(w[])
        #r[0] = 180
        R = cv2.Rodrigues(r)[0]

        P = R[:2]
        #upper_or_down = np.array([-1, -1, -1, 1, -1, 1, 1, 1, 1, 1])
        # skull_upper_or_down = np.array([-1,1,1,1,1])
        skull_upper_or_down = np.array([1,-1, 1, 1, 1, 1])
        shape3D = self.mean3D.copy()
        for i,blendshape in enumerate(self.blendshapes):# 10 changed
        #for i, blendshape in enumerate(self.blendshapes):
            print(len(self.blendshapes))
            #print(self)
            print(w[i])

            print(skull_upper_or_down[i])
            for v in blendshape:


                shape3D[int(v[0])] = skull_upper_or_down[i] * w[i] * self.mean3D[int(v[0])]  * v[1:] +shape3D[int(v[0])]
        #t[1] = -1* t[1]
        projected = s * np.dot(P,shape3D.T)   + t[:,np.newaxis]
        # print("pppp")
        # print(projected.shape)
        return projected


