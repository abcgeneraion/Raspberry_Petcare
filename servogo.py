#!/usr/bin/env python
# coding: utf-8


import RPi.GPIO as GPIO
import time

degree1 = 0
degree2 = 0
servopin = 5
servopin2 = 13

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([servopin, servopin2], GPIO.OUT, initial=False)
p = GPIO.PWM(servopin, 50)  # 50HZ
p2 = GPIO.PWM(servopin2, 50)  # 50HZ
p.start(0)
p2.start(0)
time.sleep(1)

class Servo(object):
    def __init__(self, string):
        global degree1, degree2
        if string=='up':
            turn_up(degree1)
            if degree1 !=-20:degree1-=20
        elif string=='down':
            turn_down(degree1)
            if degree1 !=140:degree1+=20
        elif string=='left':
            turn_left(degree2)
            if degree2 !=-40:degree2-=20
        elif string=='right':
            turn_right(degree2)
            if degree2 !=120:degree2+=20



def turn_up(i):
    print("degree1:{}".format(i))
    p.ChangeDutyCycle(float(i)/18 + 2.5)  # 设置转动角度
    time.sleep(0.02)  # 等该20ms周期结束
    p.ChangeDutyCycle(0)  # 归零信号
    time.sleep(0.2)


def turn_down(i):
    print("degree1:{}".format(i))
    p.ChangeDutyCycle(float(i)/18 + 2.5)  # 设置转动角度
    time.sleep(0.02)  # 等该20ms周期结束
    p.ChangeDutyCycle(0)  # 归零信号
    time.sleep(0.2)

def turn_left(i):
    print("degree2:{}".format(i))
    p2.ChangeDutyCycle(float(i)/18 + 2.5)  # 设置转动角度
    time.sleep(0.02)  # 等该20ms周期结束
    p2.ChangeDutyCycle(0)  # 归零信号
    time.sleep(0.2)

def turn_right(i):
    print("degree2:{}".format(i))
    p2.ChangeDutyCycle(float(i)/18 + 2.5)  # 设置转动角度
    time.sleep(0.02)  # 等该20ms周期结束
    p2.ChangeDutyCycle(0)  # 归零信号
    time.sleep(0.2)


