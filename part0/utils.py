import numpy as np
def Homogeneous(data):
    ones = np.ones((1,data.shape[0]))
    data = np.column_stack((data,ones.T))
    return  data

def normalization(data):  #[-1,1]
    _range = np.max(abs(data))
    if _range  < 0.1:
        return np.zeros_like(data)
    return data / _range
