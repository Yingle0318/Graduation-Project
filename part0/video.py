import cv2
import numpy as np
def video():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))
    while(cap.isOpened()):
        ret,frame = cap.read()
        if ret == True:
            frame = cv2.flip(frame,2)
            out.write(frame)
            cv2.imshow('frame',frame)
            if cv2.waitKey(2) == ord('q'):
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
def picture():
    cap = cv2.VideoCapture(0)
    i = 0
    while (1):
        ret, frame = cap.read()
        k = cv2.waitKey(1)
        if k == 27:
            break
        elif k == ord('s'):
            cv2.imwrite('D:\A_study\projects\Graduation Project' + str(i) + '.jpg', frame)
            i += 1
        cv2.imshow("capture", frame)
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    picture()