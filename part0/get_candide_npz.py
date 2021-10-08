import numpy as np

VERTEX_LIST = np.loadtxt('VERTEX LIST.txt',skiprows=2,comments='#')
#print(VERTEX_LIST)
FACE_LIST = np.loadtxt('FACE LIST.txt',skiprows=2,comments='#')

print(FACE_LIST)
print(FACE_LIST.shape)
SHAPE_UNIT_LIST = np.loadtxt("SHAPE UNIT LIST.txt",skiprows=2,comments='#')
print(SHAPE_UNIT_LIST)
print(SHAPE_UNIT_LIST.shape)

ANIMATION_UNITS_LIST = np.loadtxt("ANIMATION UNITS LIST.txt",skiprows=2,comments='#')
#print(ANIMATION_UNITS_LIST)
#print(ANIMATION_UNITS_LIST.shape)
# 0-9 Upper lip raiser (AU10)
# 10 -21 Jaw drop (AU26/27)
# 22 - 39 Lip stretcher (AU20)
#40-53  AUV3   Brow lowerer (AU4)
#54-67 AUV14 Lip corner depressor (AU13/15)
#68-75    AUV5   Outer brow raiser (AU2)
#76-87        AUV6   Eyes closed (AU42/43/44/45)
np.savez('candide_wfm',VERTEX_LIST = VERTEX_LIST,FACE_LIST =FACE_LIST,SHAPE_UNIT_LIST = SHAPE_UNIT_LIST,ANIMATION_UNITS_LIST = ANIMATION_UNITS_LIST)

