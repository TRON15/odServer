# encoding:utf-8
import cv2
import numpy as np
from bottle import route,request,response,static_file
from pos_info import findSpot
import time
import threading

global t_flag
t_flag = 0

def pos_info_thr():
    global g_frame
    global pflag
    global t_flag
    t_flag = 1
    while(1 and g_ret):
        ret, frame = cap.read()
        frame = frame[0:450, 190:500]
        while(pflag):
            continue
        pflag = 1
        if(g_ret):
            g_frame = frame
        pflag = 0
        # print('get finished')
    t_flag = 0

@route('/server_func/cap_open', method = 'POST')
def cap_open():
    global cap
    global pflag
    global thr
    global g_ret
    global t_flag
    g_ret = True
    pflag = 0
    print('pflag', pflag)
    if (t_flag == 0):
        cap = cv2.VideoCapture(0)
        thr = threading.Thread(target = pos_info_thr)
        thr.setDaemon(True)
        thr.start()
        print('threading starts')
    res = {'result':'camrea 0 has been opened'}
    response.content_type = 'application/json'
    return res

@route('/server_func/cap_release', method = 'POST')
def cap_release():
    global thr
    global cap
    global g_ret
    g_ret = False
    print('over')
	# sleep to wait the thr find g_ret = False
    time.sleep(0.5)
    cap.release()
    res = {'result':'camrea 0 has been released'}
    response.content_type = 'application/json'
    return res

@route('/server_func/upload_info', method = 'POST')
def upload_info():
    redBlock = request.json[u'redBlock']
    blackBlock = request.json[u'blackBlock']
    # store it in block_pos.py
    f=open('block_pos.py','r')
    flist=f.readlines()
    f.close()
    red_config_str = 'redPos = {_redBlock}\n'
    black_config_str = 'blackPos = {_blackBlock}\n'
    red_config_str = red_config_str.format(_redBlock = redBlock)
    black_config_str = black_config_str.format(_blackBlock = blackBlock)
    flist[0] = red_config_str
    flist[1] = black_config_str
    with open('block_pos.py','rw+') as f:
        f.seek(0)  
        f.truncate(0)
        f.writelines(flist) 
        f.close()
    res = {'result':'upload success!'}
    response.content_type = 'application/json'
    return res

@route('/server_func/refresh_frame', method = 'POST')
def refresh_frame():
    global pflag
    while(pflag):
        continue
    pflag = 1
    frame = g_frame
    pflag = 0
    cv2.imwrite('/tmp/frame.png', frame)
    img= open('/tmp/frame.png').read().encode('base64')
    res = {'frame':img}
    response.content_type = 'application/json'
    return res

@route('/server_func/pos_info', method = 'POST')
def pos_info():
    from block_pos import redPos
    from block_pos import blackPos
    global pflag
    print('pre')
    while(pflag):
        continue
    pflag = 1
    print('get frame')
    frame = g_frame
    pflag = 0
    st_pro = time.time()
    spots, area, r = findSpot(frame, 175, 3.2, 3, 110, 35)
    # show spots
    for _spot in spots:
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
    wt0 = time.time()
    cv2.imwrite('/tmp/frame.png', frame)
    wt1 = time.time()
    print('writetime',wt1-wt0)
    bt0=time.time()
    img= open('/tmp/frame.png').read().encode('base64')
    bt1= time.time()
    print('png2buffer', bt1-bt0)
    res = {'spots':spots, 'red_block':redPos, 'black_block':blackPos, 'frame':img}
    _ed_pro = time.time()
    print('processing+tolist', _ed_pro-st_pro)
    response.content_type = 'application/json'
    return res
