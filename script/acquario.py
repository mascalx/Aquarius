#!/usr/bin/env python
#-*- coding: utf-8 -*-

# ** AQUARIUS **
# Written by Carlo Mascellani
# Last update 27/03/2017

import os, glob, subprocess, time, string, sys, datetime
from w1thermsensor import W1ThermSensor
from gpiozero import RGBLED, LED, PWMLED
from picamera import Color
# Import for graphic display
import TFT as GLCD
import ImageFont
import Image
import ImageDraw
#TFT to RPi connections
# PIN   TFT         RPi
# 1     backlight   (GPIO 26)
# 2     MISO        <none>
# 3     CLK         (GPIO 11)
# 4     MOSI        (GPIO 10)
# 5     CS-TFT      (GPIO 5)
# 6     CS-CARD     <none>
# 7     D/C         (GPIO 6)
# 8     RESET       (none)
# 9     VCC         3V3
# 10    GND         GND

MODE = 0 # Use RGB led strips for lighting. Put 1 for on/off lamps
PWMF = 1 # Use standard pwm for RGB led strip. Put 1 to use PWMLed with different frequency set

# Configuration defaults
t_fan_on = 25 # Temp for starting the fan
t_fan_off = 20 # Temp to stop the fan
t0 = "20:00" # Time for night light (end of sunset)
rgb0 = "#000000" # Night light (#RRGGBB)
t1 = "08:00" # Time for dawn (end of night)
rgb1 = "#996633" # Dawn light (#RRGGBB)
t2 = "08:30" # Time for daylight (end of dawn)
rgb2 = "#ffffaa" # Day light (#RRGGBB)
t3 = "19:30" # Time for sunset (end of daylight)
rgb3 = "#aaaa77" # Sunset color (#RRGGBB)
t_fade = 5 # Light fading duration
t_cibo=2 # Food motor on duration
tf1 = "11:50" # Lunch time, so stop fan
tf2 = "12:10" # End of lunch time, so fan can work again

# Hardware settings
fan = LED(25) # Water cooling fan
cpufan = LED(12) # System cooling fan
if (MODE==0):
    if (PWMF==0):
        led = RGBLED(red=17, green=18, blue=27) # RGB leds strip
    else:
        ledr=PWMLED(17,frequency=500);
        ledg=PWMLED(18,frequency=500);
        ledb=PWMLED(27,frequency=500);
else:
    lamp1 = LED(17) # First lamp relay
    lamp2 = LED(18) # Second lamp relay
    lamp3 = LED(27) # Third lamp relay

backlight = PWMLED(26,frequency=500) # LCD backlight
sensor = W1ThermSensor() # Temperature sensor

# Reboot the system
def RestartFunc():
    os.system("sudo reboot")
    return
    
# Halt the system
def StopFunc():
    os.system("sudo /sbin/shutdown -hP now")
    return
    
# Update the system
def UpdateFunc():
    os.system("sudo apt-get -y update")
    return
    
# Write the configuration file
def WriteConfig():
    file = open("/home/pi/acquario.cfg", "w")
    file.write(t_fan_on.str()+'\n')
    file.write(t_fan_off.str()+'\n')
    file.write(t0+'\n')
    file.write(rgb0+'\n')
    file.write(t1+'\n')
    file.write(rgb1+'\n')
    file.write(t2+'\n')
    file.write(rgb2+'\n')
    file.write(t3+'\n')
    file.write(rgb3+'\n')
    file.write(t_fade.str()+'\n')
    file.write(tf1+'\n')
    file.write(tf2+'\n')
    file.close()
    return
    
# Read the configuration file    
def ReadConfig():
    global t_fan_on, t_fan_off, t0, t1, t2, t3
    global rgb0, rgb1, rgb2, rgb3, t_fade, t_cibo
    try:
        file = open("/home/pi/acquario.cfg", "r")
        t_fan_on=int(file.readline())
        t_fan_off=int(file.readline())
        t0=file.readline()
        rgb0=file.readline()[:7]
        t1=file.readline()
        rgb1=file.readline()[:7]
        t2=file.readline()
        rgb2=file.readline()[:7]
        t3=file.readline()
        rgb3=file.readline()[:7]
        t_fade=int(file.readline())
        tf1=file.readline()
        tf2=file.readline()
        file.close()
    except:
        pass    
    return

# Write the text on the display  
def DisplayText(disp,draw,x,y,txt,size,color,clear=True):
    if (clear):
        disp.clear()
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', size)
    draw.text((x, y), txt, font=font, fill=color)
    return
    
# Set strip color
def SetStripColor(color1):
    #backlight.value = Color(color1).lightness
    try:
        if (PWMF==0):
            led.color=Color(color1)
        else:
            ledr.value=Color(color1).red
            ledg.value=Color(color1).green
            ledb.value=Color(color1).blue
    except:
        pass
    return
    
# Feed the fish    
def Nutre():
    food.forward()
    time.sleep()
    food.stop(t_cibo)
    return

# Returns time object from string HH:MM
def GetTime(t):
    try:
        return datetime.time(int(t[:2]),int(t[-2:]))
    except:
        return datetime.datetime.now().time()

# Update the web pages
def DataUpdate(t):
    try:
        tt="{:.1f}".format(t)
        file = open("/var/www/data.php", "w")
        file.write('<?php $output=\'<html><body style="margin:0;padding:0;">\';')
        file.write('$temp="'+tt+'";')
        file.write('$output=$output.\'<p style="color:white;font-size:18px;">\'.date("d/m/Y H:i").\'</p>\';')
        file.write('$output=$output.\'<p style="color:white;margin:0;padding:0;font-size:18px;">Temperatura acqua:<br/><span style="color:white;font-size:32px;"><b>\'.$temp.\'&deg;C</b></span></p>\';')
        file.write('$output=$output.\'</html></body>\';')
        file.write('echo $output;?>')
        file.close()
    except:
        pass
    return

# Read CPU temperature
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    temp =(res.replace("temp=","").replace("'C\n",""))
    return float(temp)
        
# Main program
if __name__ == '__main__':
    # Setup the display    
    disp = GLCD.TFT()		# Create TFT LCD display class.
    disp.initialize()		# Initialize display.
    disp.clear()			# Alternatively can clear to a black screen by calling:
    draw = disp.draw()		# Get a PIL Draw object to start drawing on the display buffer
    backlight.on()
    dd=u"\u2103"
    
    while True:
        # Get updated configuration
        ReadConfig();
        # Shows current date and time
        DisplayText(disp,draw,10,30,time.strftime("%d/%m/%Y %H:%M"),14,(255,255,0))
        # Reads temperature and shows it
        try:
            t=sensor.get_temperature()
        except:
            pass
        DisplayText(disp,draw,5,70,"{:.1f}".format(t)+dd,38,(255,255,255),clear=False)
        # Update display
        disp.display()
        DataUpdate(t)
        
        # Get time of the day
        minuti = datetime.datetime.now().time()
        
        # Check the temperature to drive the fan (disable if "lunch" time)
        if (minuti<GetTime(tf1)) or (minuti>GetTime(tf2)):
            if (t>t_fan_on):
                fan.on()
            if (t<t_fan_off):
                fan.off()
        else:        
            fan.off()
            
        # Check CPU temperature to drive the cooling fan
        tc = getCPUtemperature()
        if (tc>55):
            cpufan.on()
        if (tc<45):
            cpufan.off()
            
        # Checks time of day and set the right color
        if (MODE==0): # Using RGB leds
            if (minuti<GetTime(t1)):
                SetStripColor(rgb0) # Night
            elif (minuti<GetTime(t2)):
                SetStripColor(rgb1) # Sunrise
            elif (minuti<GetTime(t3)):
                SetStripColor(rgb2) # Day
            elif (minuti<GetTime(t0)):
                SetStripColor(rgb3) # Sunset
            else:
                SetStripColor(rgb0) # Night
        else: # Using on/off lamps
            if (minuti<GetTime(t1)):  # Night
                lamp1.off()
                lamp2.off()
                lamp3.off()
            elif (minuti<GetTime(t2)): # Dawn
                lamp1.on()
                lamp2.off()
                lamp3.off()
            elif (minuti<GetTime(t3)): # Day
                lamp1.on()
                lamp2.on()
                lamp3.off()
            elif (minuti<GetTime(t0)): # Sunset
                lamp1.on()
                lamp2.off()
                lamp3.off()
            else: # Night
                lamp1.off()
                lamp2.off()
                lamp3.off()

        time.sleep(1) # Wait 1 second
