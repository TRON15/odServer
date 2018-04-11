import cv2
def get_BGR(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print([y, x],frame[y, x])
##cap = cv2.VideoCapture(0)
cv2.namedWindow('frame')
cv2.setMouseCallback('frame',get_BGR)
#frame=cv2.imread('pic/neo/frame250.png')
# frame = frame[0:450, 190:500]
cap = cv2.VideoCapture(0)
while (True):
    ret, frame = cap.read()
    frame = frame[0:450, 190:500]
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
