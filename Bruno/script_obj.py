import os
import numpy as np
class Pig:
    def __init__(self,objFilePath):
#objFilePath = 'D:\A_study\projects\Graduation Project\Bruno\Pig(1).obj'
        with open(objFilePath) as file:
            points = []
            while 1:
                line = file.readline()
                if not line:
                    break
                strs = line.split(" ")
                if strs[0] == "v":
                    points.append((float(strs[1]), float(strs[2]), float(strs[3])))


# points原本为列表，需要转变为矩阵，方便处理

if __name__ == "__main__":
    objFilePath = 'D:\A_study\projects\Graduation Project\Bruno\Pig(1).obj'
