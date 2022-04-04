import RGB_Lib
led = RGB_Lib.Programing_RGB()
led.Set_All_RGB(255, 255, 255)

import cv2
import numpy as np
import jetbot
bot = jetbot.Robot()
cam = jetbot.Camera(width=640, height=640)

led.Set_All_RGB(255, 0, 0)

import hand_detect

led.Set_All_RGB(0, 255, 0)



# ##저장 코드
# import os
# os.makedirs('saved', exist_ok=True)
# import time
# import random
# ###

def get_biggest(det):
    w = det[:, 2] - det[:, 0]
    h = det[:, 3] - det[:, 1]
    size = w * h
    max_index = np.argmax(size)
    return det[max_index]


def decode_det(obj, width=640, height=640): #width, height of input image
    x1, y1, x2, y2, conf, cat = obj
    cx = (x1 + x2) / 2 #center of object
    cy = (y1 + y2) / 2 #center of object
    w = x2 - x1 #width of object
    h = y2 - y1 #heighth of object
    
    #distance from camera
    dist = width / w
    #pixel offset from center    
    offx = cx - width / 2
    #angle
    ang = np.arctan2(dist, offx)
    
    return cx, cy, w, h, dist, offx, ang
    
power = 0.8
while True:
    frame = cam.value
    # path = time.strftime('saved/%H%M%S_' + str(random.randint(0, 1000)) + '.jpg')
    # cv2.imwrite(path, frame)
    
    det = hand_detect.detect(frame).to('cpu').numpy()
    
    if len(det) == 0:
        print('no object found')
        led.Set_All_RGB(0, 255, 0)
        bot.forward(0)
        continue
    biggest = get_biggest(det)###################
    cat = biggest[5]######################
    code = decode_det(biggest)############
    print(cat)
    
    if len(det) == 1:
        #left
        if cat == 0:
            #bot.left(power)
            bot.set_motors(0.4, 0.7)
            led.Set_All_RGB(255, 255, 0)
        elif cat == 1:
            #bot.right(power)
            bot.set_motors(0.7, 0.4)
            led.Set_All_RGB(0, 255, 255)
        elif cat == 2:
            bot.forward(power)           
            led.Set_All_RGB(255, 0, 0)
        elif cat == 3:
            bot.backward(power)
            led.Set_All_RGB(0, 0, 255)

        else:
            bot.forward(0)
            led.Set_All_RGB(0, 255, 0)
    
    if len(det) == 2:

        if det[0, 5] == 0 and det[1, 5] == 0:
            #bot.left(power)
            bot.set_motors(0.1, 0.7)
            led.Set_All_RGB(255, 255, 0)

        if det[0, 5] == 1 and det[1, 5] == 1:
            #bot.right(power)
            bot.set_motors(0.7, 0.1)
            led.Set_All_RGB(0, 255, 255)

        #if det[0, 5] == 4 and det[1, 5] == 4:
         #   break
        
bot.forward(0)
print('done.')
led.Set_All_RGB(0, 0, 0)