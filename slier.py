import cv2
import time
# 创建窗口



def do_something():

    print('Button Pressed!!')
    print('Do Something')


def update(x):
    if x == 1:
        do_something()
        #cv2.waitKey(500)
        #cv2.setTrackbarPos('button', 'image_win', 0)


image = cv2.imread("pictures/Graduation Project1.jpg")
print(image.shape)

cv2.namedWindow('image_win')
cv2.imshow("image_win",image)

cv2.createTrackbar('button','image_win',0,1,update)
#cv2.setTrackbarPos('button','image_win', 1)
# 等待按键按下
cv2.waitKey(0)
# 销毁窗口
cv2.destroyAllWindows()