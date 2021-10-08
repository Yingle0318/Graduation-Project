import numpy as np
from OpenGL.GL import *

def load_A_B():
    Animation_units = np.load("modelsChanged.npz", allow_pickle=True)
    base = np.load("base.npz", allow_pickle=True)
    B = base['arr_0']
    A = Animation_units['arr_0']
    return A ,B


if __name__ == "__main__":
    A , B = load_A_B()



