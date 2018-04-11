import numpy as np
import cv2
import time
from block_pos import redPos
from block_pos import blackPos

def get_median(data):
    if(len(data) == 0):
        return
    data.sort()
    half = len(data) // 2
    return (data[half] + data[~half]) / 2

def error_equal(pos1, pos2, error_limit):
    if(len(pos1) != len(pos2)):
        return 0
    else:
        for i in range(0,len(pos1)):
            if(abs(pos1[i]-pos2[i]) > error_limit):
                return 0
    return 1
    
def draw_rect(frame, num, points, color, width):
    for i in range(0,num): 
        cv2.line(frame, (int(points[i%num][0]),int(points[i%num][1])), (int(points[(i+1)%num][0]),int(points[(i+1)%num][1])), color, width)
    return frame

# findSpot
# bounds are used to pick up real spots instead of stray light
# 0~150 en*
def findSpot(frame, binary_bound, area_bound, error_limit, black_C, red_C):
    # BGR to gary
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh =  cv2.threshold(gray, binary_bound, 255, cv2.THRESH_BINARY)
    
    black_part = gray[(blackPos[0][1]):(blackPos[1][1]), (blackPos[0][0]):(blackPos[1][0])]
    ret, thresh_black_part =  cv2.threshold(black_part, (binary_bound-black_C), 255, cv2.THRESH_BINARY)
    # thresh_black_part = cv2.adaptiveThreshold(black_part,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,7, -black_C)
    
    red_part = gray[(redPos[0][1]):(redPos[1][1]), (redPos[0][0]):(redPos[1][0])]
    # ret, thresh_red_part =  cv2.threshold(red_part, (binary_bound+red_C), 255, cv2.THRESH_BINARY)
    thresh_red_part = cv2.adaptiveThreshold(red_part,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,7,-red_C)
    
    thresh[(blackPos[0][1]):(blackPos[1][1]), (blackPos[0][0]):(blackPos[1][0])] = thresh_black_part
    thresh[(redPos[0][1]):(redPos[1][1]), (redPos[0][0]):(redPos[1][0])] = thresh_red_part
    
    image,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # get position of spot
    temp_store = []
    temp_area = []
    spot = []
    area = []
    r = []
    # pang!
    centre = []
    for cnt in contours:
        # print(type(cnt))
        # print('cnt',cnt)
        M = cv2.moments(cnt)
        if(M['m00']>0):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            centre.append([cnt, [cx, cy], True])
        else:
            (x,y), radius = cv2.minEnclosingCircle(cnt)
            centre.append([cnt, [x, y], True])
    neo_cnt = []
    j = 0
    flag = 0
    max_num_sq =2
    
    while(flag != len(centre)):
        tmp = []
        while(centre[j][2] == False):
            j = j+1
        tmp.extend(centre[j][0])
        centre[j][2] = False
        flag = flag+1
        num_sq = 1
        for i in range((j+1), len(centre)):
            if(centre[i][2]):
                if( error_equal(centre[j][1], centre[i][1], error_limit) ):
                    tmp.extend(centre[i][0])
                    centre[i][2] = False
                    flag = flag+1
                    num_sq = num_sq+1
            if(num_sq == max_num_sq ):
                break
        neo_cnt.append(np.array(tmp))
        j = j+1
    for cnt in neo_cnt:
        M = cv2.moments(cnt)
        (x,y), radius = cv2.minEnclosingCircle(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        aspect_ratio = float(w)/h
        # print(M['m00'], (x,y), radius, aspect_ratio)
        if( (M['m00'] > area_bound) and (0.2<aspect_ratio<5) ):
            # print('hhh', M['m00'], (x,y), radius, aspect_ratio)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            temp_store.append([[cx, cy], M['m00'], radius])
            temp_area.append(M['m00'])
    # find traitor
    mid_area = get_median(temp_area)
    for tmp in temp_store:
        # upper may be changed by the guangqiang
        if( mid_area*0.23 < tmp[1] < mid_area*8 ):
            pass
        else:
            temp_store.remove(tmp)
    for tmp in temp_store:
        spot.append(tmp[0])
        area.append(tmp[1])
        r.append(tmp[2])
    return spot, area, r
# find blocks position
def findBlockPos(frame, Lower, Upper):
    _frame = cv2.inRange(frame, Lower, Upper)
    (_, cnts, _) = cv2.findContours(_frame.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    for cnt in cnts:
        M = cv2.moments(cnt)
        if (M['m00']>area):
            area = M['m00']
            target_cnt =cnt
    points = cv2.boxPoints(cv2.minAreaRect(target_cnt))
    M = cv2.moments(points)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return [cx, cy], points
