import numpy as np
import cv2
cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
#x = cap.get(cv2.CAP_PROP_EXPOSURE)
#print(x)
num = 200
while(num):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # basic info of the frame
    shape = frame.shape
    h=shape[0]
    w=shape[1]
    # show the RGB of the middle point
    print(h,w,frame[h/2,w/2])
    # show the middle area of the frame
    # cv2.circle(frame,(int(w/2),int(h/2)), 5, (0,0,255), 2)
    # processing, to get the RGB of the centre of the frame
    cv2.imshow('frame',frame)
    storetext = '../pic/neo_1/frame{_num}.png'
    storetext = storetext.format(_num=num)
    cv2.imwrite(storetext,frame)
    num=num-1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
