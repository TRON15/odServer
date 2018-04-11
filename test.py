import numpy as np
import cv2
import pos_info
from pos_info import findSpot
from pos_info import findBlockPos
from pos_info import draw_rect
from block_pos import redPos
from block_pos import blackPos
import time
# load frame

def frame_processing(frame):
    t0 = time.time()
    # get spots info
    spot, area, r = findSpot(frame, 175 , 3.2, 3, 110, 35)
    print('--------')
    print('Information of spots:')
    for i in range(0, len(spot)):
        print('point:', (i+1), 'pos:', spot[i], 'area:', area[i], 'radius:', r[i])
    print('--------')
    # get red block info
    print('Information of red Bloc:')
    print('The centre of red Block:', redPos)
    print('--------')
    # get black block info
    print('Information of black Block:')
    print('The centre of black Block:', blackPos)
    print('--------')
    # show them in picture
    # show spots
    for _spot in spot:
        cv2.circle(frame, (_spot[0], _spot[1]), 2, (0, 255, 0), -1)
        text = '({posx},{posy})'
        text = text.format(posx = _spot[0], posy = _spot[1])
        cv2.putText(frame, text, (_spot[0]+15, _spot[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 255, 0), 1)
    # show red block
    redcen = [ int((redPos[0][0]+redPos[1][0])/2),int((redPos[0][1]+redPos[1][1])/2)]
    cv2.circle(frame,(redcen[0], redcen[1]), 3, (0, 0, 255), -1)
    cv2.rectangle(frame, (redPos[0][0], redPos[0][1]), (redPos[1][0], redPos[1][1]),(0, 0, 255),2)
    text = '({posx},{posy})'
    text = text.format(posx = redcen[0], posy = redcen[1])
    # cv2.putText(frame, text, (redcen[0]-4, redcen[1]+16), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 0, 255), 1)
    # show black block
    blackcen = [int((blackPos[0][0]+blackPos[1][0])/2), int((blackPos[0][1]+blackPos[1][1])/2)]
    cv2.circle(frame,(blackcen[0], blackcen[1]), 3, (0, 255, 255), -1)
    cv2.rectangle(frame, (blackPos[0][0], blackPos[0][1]), (blackPos[1][0], blackPos[1][1]),(0, 255, 255),2)
    text = '({posx},{posy})'
    text = text.format(posx = blackcen[0], posy = blackcen[1])
    # cv2.putText(frame, text, (blackcen[0]-4, blackcen[1]+16), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 255, 255), 1)
    t1 = time.time()
    print('func_time',t1-t0)
    return frame
cap = cv2.VideoCapture(0)
while(1):
    ret, frame = cap.read()
    frame = frame[0:450, 190:500]
    frame_processed = frame_processing(frame)
    cv2.imshow('frame_processed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
