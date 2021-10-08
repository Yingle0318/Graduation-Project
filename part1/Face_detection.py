import cv2
import dlib
import numpy as np

def face_detect(color_image):
    #color_image = cv2.imread(file_path)
    #color_image = cv2.resize(color_image,None, fx=2, fy=2) #放大3倍
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)  # 将彩色图片转换为灰色图片，提高人脸检测的准确率

    # 也可以不用转换灰色图像，但是BGR要转换为RGB
    # color_image = cv2.imread(file_path, cv2.IMREAD_COLOR)
    # B, G, R = cv2.split(color_image)   # 分离三个颜色通道
    # color_image = cv2.merge([R, G, B]) # 融合三个颜色通道生成新图片

    # 人脸检测器
    detector = dlib.get_frontal_face_detector()
    # 特征点检测器
    predictor = dlib.shape_predictor("D:\A_study\projects\Graduation Project\shape_predictor_68_face_landmarks.dat")
    # 检测人脸
    # The 1 in the second argument indicates that we should upsample the image 1 time.
    faces = detector(gray_image, 1)

    # 调用训练好的卷积神经网络（cnn）模型进行人脸检测
    # cnn_face_detector = dlib.cnn_face_detection_model_v1('model/mmod_human_face_detector.dat')
    # faces = cnn_face_detector(gray_image, 1)

    for face in faces:
        # 用矩形框住人脸
        left = face.left()
        top = face.top()
        right = face.right()
        bottom = face.bottom()
        cv2.rectangle(color_image, (left, top), (right, bottom), (0, 255, 0), 2)



        pts = np.array([[left,top],  [right, top], [right, bottom],[left , bottom]], np.int32)
        #copy_pts = pts
        pts = pts.reshape((-1, 1, 2))

        cv2.polylines(color_image, [pts], True, (0, 255, 255))
        # 寻找人脸的68个标定点
        shape = predictor(color_image, face)
        # 遍历所有点，打印出其坐标，并圈出来
        for idx, pt in enumerate(shape.parts()):
            pt_pos = (pt.x, pt.y)
            # 参数分别为：图像，圆心坐标，半径，颜色，线条粗细   # HL
            cv2.circle(color_image, pt_pos, 2, (0, 0, 255), -1)
            # 利用cv2.putText输出1-68
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(color_image, str(idx + 1), pt_pos, font, 0.3, (255, 0, 0), 1, cv2.LINE_AA)
            # 位置，字体，大小，颜色，字体厚度

    cv2.imshow("Image", color_image)

def main():
    cap = cv2.VideoCapture("D:\A_study\projects\Graduation Project\my_test_video.avi")
    while (1):
        # get a frame
        ret, frame = cap.read()
        # show a frame
        face_detect(frame)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()