import Adafruit_GPIO as GPIO

class Programing_RGB(object):
        
    def get_i2c_device(self,address, i2c, i2c_bus):
        if i2c is not None:
            return i2c.get_i2c_device(address)
        else:
            import Adafruit_GPIO.I2C as I2C
            if i2c_bus is None:
                return I2C.get_i2c_device(address)
            else:
                return I2C.get_i2c_device(address, busnum=i2c_bus)
        
    def __init__(self):
        # Create I2C device.
        #"""Initialize the RGB."""
        # Setup I2C interface for the device.
#         if i2c is None:
#             import Adafruit_GPIO.I2C as I2C
#             i2c = I2C
        self._device = self.get_i2c_device(0x1b, None, 1)
    
    def Set_All_RGB(self, R_Value, G_Value, B_Value):
        try:
            self._device.write8(0x00,0xFF)
            self._device.write8(0x01,R_Value)
            self._device.write8(0x02,G_Value)
            self._device.write8(0x03,B_Value)
        except:
            print ('Set_All_RGB I2C error')
    
    def OFF_ALL_RGB(self):
        try:
            self.Set_All_RGB(0x00,0x00,0x00)
        except:
            print ('OFF_ALL_RGB I2C error')
    
    def Set_An_RGB(self, Position, R_Value, G_Value, B_Value):
        try:
            if(Position <= 0x09):
                self._device.write8(0x00,Position)
                self._device.write8(0x01,R_Value)
                self._device.write8(0x02,G_Value)
                self._device.write8(0x03,B_Value)
        except:
            print ('Set_An_RGB I2C error')
    def Set_WaterfallLight_RGB(self):
        try:
            # self.OFF_ALL_RGB()
            self._device.write8(0x04, 0x00)
        except:
            print ('Set_WaterfallLight_RGB I2C error')
    def Set_BreathColor_RGB(self):
        try:
            # self.OFF_ALL_RGB()
            self._device.write8(0x04, 0x01)
        except:
            print ('Set_BreathColor_RGB I2C error')
    def Set_ChameleonLight_RGB(self):
        try:
            # self.OFF_ALL_RGB()
            self._device.write8(0x04, 0x02)
        except:
            print ('Set_ChameleonLight_RGB I2C error')
    #确保颜色值在0-6中
    def Set_BreathSColor_RGB(self, color):
        try:
            self._device.write8(0x05, color)
        except:
            print ('Set_BreathSColor_RGB I2C error')
    #确保速度设置值在1,2,3中
    def Set_BreathSSpeed_RGB(self, speed):
        try:
            self._device.write8(0x06, speed)
        except:
            print ('Set_BreathSSpeed_RGB I2C error')
    def Set_BreathSLight_RGB(self):
        try:
            # self.OFF_ALL_RGB()
            self._device.write8(0x04, 0x03)
        except:
            print ('Set_BreathSLight_RGB I2C error')

rgb = Programing_RGB()
rgb.Set_All_RGB(255, 0, 0)

import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

rgb.Set_BreathColor_RGB()

from jetbot.utils.utils import get_ip_address

rgb.Set_All_RGB(255, 255, 0)

import subprocess
import time

disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=0, gpio=1)
disp.begin()

disp.clear()
disp.display()

rgb.Set_All_RGB(255, 255, 255)

disp_image = Image.new('1', (disp.width, disp.height))

screen = ImageDraw.Draw(disp_image)
screen.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)


screen_padding= -2
screen_top = screen_padding
screen_bottom = disp.height - screen_padding
screen_x = 0

font = ImageFont.load_default()

def getip():
    return str(get_ip_address('wlan0'))


def ShowInfo(strInfo):
    rgb.Set_All_RGB(0, 0, 0)
    screen.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)

    # if you want to print a message on the top line.
    # screen.text((screen_x, screen_top+0), strInfo, font=font, fill=255)

    rgb.Set_All_RGB(255, 0, 0)
    # else print cpu info
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    Cpu = subprocess.check_output(cmd, shell = True)
    screen.text((screen_x, screen_top+0), str(Cpu.decode('utf-8')), font=font, fill=255)

    rgb.Set_All_RGB(255, 255, 0)
    #2 ip
    screen.text((screen_x, screen_top+8), "IP:" + getip(), font=font, fill=255)
   
    rgb.Set_All_RGB(255, 255, 255)
    #3 mem
    cmd = "free -m | awk 'NR==2{printf \"Mem:%s/%sM %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True)
    screen.text((screen_x, screen_top+16), str(MemUsage.decode('utf-8')), font=font, fill=255)

    rgb.Set_All_RGB(0, 255, 0)
    #4 disk
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk:%d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)
    screen.text((screen_x, screen_top+25), str(Disk.decode('utf-8')), font=font, fill=255)

    rgb.Set_All_RGB(0, 0, 255)
    disp.image(disp_image)
    disp.display()
    rgb.Set_All_RGB(0, 255, 255)

# rgb.Set_BreathColor_RGB()

while True:
    ShowInfo("My Message")
    time.sleep(1)


#run it with boot
#https://stackoverflow.com/questions/24518522/run-python-script-at-startup-in-ubuntu    