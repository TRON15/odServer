# -*- coding: utf-8 -*-
import requests
import json
import time
# basic info of the server
server_address = '192.168.0.101'
headers = {'content-type':'application/json'}

#open cap
def open_cap():
    '''
    payload = {}
    r = requests.post('http://'+server_address+':18888/server_func/cap_open', data=json.dumps(payload), headers=headers)
    time.sleep(1)
    return (r.json()['result'])
    '''
    return 'open'

# refresh /tmp/frame.png
def refresh_frame():
    '''
    payload = {}
    r = requests.post('http://'+server_address+':18888/server_func/refresh_frame', data=json.dumps(payload), headers=headers)
    # get new frame
    img = r.json()['frame']
    frame = img.decode('base64')
    tmp_frame = open('/tmp/frame.png','w')
    tmp_frame.write(frame);
    tmp_frame.close()
    '''

# upload block_info
def upload_block_info(redBlock, blackBlock):
    '''
    payload = {'redBlock': redBlock, 'blackBlock': blackBlock}
    r = requests.post('http://'+server_address+':18888/server_func/upload_info', data=json.dumps(payload), headers=headers)
    return (r.json()['result'])
    '''
    return 'upload success'

# close cap
def close_cap():
    '''
    payload = {}
    time.sleep(0.5)
    r = requests.post('http://'+server_address+':18888/server_func/cap_release', data=json.dumps(payload), headers=headers)
    return (r.json()['result'])
    '''
    return 'close'

