import dlib   #pip install dlib==19.6.1   &&  download shape_predictor_68_face_landmarks.dat

import numpy as np
import cv2


def rect_to_bb(rect): # 获得人脸矩形的坐标信息
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (x, y, w, h)
def shape_to_np(shape, dtype="int"): # 将包含68个特征的的shape转换为numpy array格式
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords
def resize(image, width=1200):  # 将待检测的image进行resize
    r = width * 1.0 / image.shape[1]
    dim = (width, int(image.shape[0] * r))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized



def feature(image):
    #######################
    #
    #
    #   想办法提速dlib
    #
    #
    ########################
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)
    shapes = []
    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = shape_to_np(shape)
        shapes.append(shape)
        (x, y, w, h) = rect_to_bb(rect)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #cv2.putText(image, "Face: {}".format(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    for shape in shapes:
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 0, 255), -1)
    cv2.imshow("Output", image)
    cv2.waitKey(0)
def Camera():

    cap = cv2.VideoCapture(0)
    #cap.set(5,60)
    while(1):
        # get a frame
        ret, frame = cap.read()
        # show a frame
        feature(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()