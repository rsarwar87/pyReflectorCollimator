#!/bin/python3
import argparse
import pprint
import sys
import time
import os
from matplotlib.pyplot import *
from numpy import *
import smbus
import cv2 as cv
import dearpygui.dearpygui as dpg

class CameraController:

    def set_focusing(self, val):
        value = (val << 4) & 0x3ff0
        data1 = (value >> 8) & 0x3f
        data2 = value & 0xf0
               # time.sleep(0.5)
        print("focus value: {}".format(val))
        # bus.write_byte_data(0x0c,data1,data2)
        os.system("i2cset -y 0 0x0c %d %d" % (data1,data2))

    def __init__(self, video_idx):
        self.video_idx = video_idx
        self.brightness = 100
        self.gamma = 100
        self.contrast = 100


        self.vid = cv.VideoCapture(video_idx)

        self.fps = self.vid.get(cv.CAP_PROP_FPS)
        ret, frame = self.vid.read()
        print("Frame Array:")
        print("Array is of type: ", type(frame))
        print("No. of dimensions: ", frame.ndim)
        print("Shape of array: ", frame.shape)
        print("Size of array: ", frame.size)
        print("Array stores elements of type: ", frame.dtype)
        self.get_resolution()
        self.declareCalibrationVariables()
        self.create_window()

    def set_resolution(self, height, width):
        self.frame_height = height
        self.frame_width = width

    def get_resolution(self):
        self.frame_height = self.vid.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.frame_width = self.vid.get(cv.CAP_PROP_FRAME_WIDTH)
        return self.frame_height, self.frame_width

    def set_fps(self, fps):
        self.fps = fps

    def get_fps(self):
        self.fps = self.vid.get(cv.CAP_PROP_FPS)
        return self.fps

    def create_window(self):
        self.cbEnableOffset = {}
        with dpg.window(label="Camera Control",min_size=(480, 640),
                        no_close=True) as self.mainForm:
            with dpg.tab_bar() as tb:
                with dpg.tab(label="Collimation Control"):
                    with dpg.collapsing_header(
                                    label="Centre position", closable=False,
                                    default_open=True) as self.cpo:
                        self.cbEnableOffset[self.cpo] = dpg.add_checkbox(
                            label="Enable Offset",
                            default_value=False,
                            callback=self._cbEnableKeys,
                            parent=self.cpo,
                            user_data=[self.cpo, 0])#,
                        self.cpoX = dpg.add_slider_int(label="X-offset", 
                                parent=self.cpo,
                                user_data=[self.cpo, 2],
                                callback=self._centre_position,
                                default_value=self.frame_width/2,
                                max_value=self.frame_width)
                        self.cpoY = dpg.add_slider_int(label="Y-offset", 
                                user_data=[self.cpo, 1],
                                callback=self._centre_position,
                                parent=self.cpo,
                                default_value=self.frame_height/2,
                                max_value=self.frame_height)
                        dpg.add_button(label="centre position",
                                       parent=self.cpo,
                                       user_data=[self.cpo, 0],
                                       callback=self._centre_position)
                    with dpg.collapsing_header(
                                    label="Circle 1", closable=False,
                                    default_open=True) as self.cir0:
                        self.cbEnableOffset[self.cir0] = dpg.add_checkbox(
                            label="Enable ",
                            default_value=False,
                            callback=self._cbEnableKeys,
                            user_data=[self.cir0, 0])#,
                        self.cirColor0 = dpg.add_color_edit(self.cbRBG[0], 
                                        #callback=sa,
                                        callback=self._coloredit,
                                        user_data=[self.cir0, 0],
                                        no_alpha= True, label="Color")
                        self.cirR0 = dpg.add_slider_int(label="Radius", 
                                        #callback=sa,
                                        callback=self._radii,
                                        user_data=[self.cir0, 0],
                                        max_value=self.frame_height/2, default_value = 20)
                        self.cirT0 = dpg.add_slider_int(label="Thickness", 
                                        callback=self._thickness,
                                        user_data=[self.cir0, 0],
                                        max_value=10, default_value = 2)
                        #dpg.add_same_line()
                    with dpg.collapsing_header(
                                    label="Circle 2", closable=False,
                                    default_open=True) as self.cir1:
                        self.cbEnableOffset[self.cir1] = dpg.add_checkbox(
                            label="Enable ",
                            default_value=False,
                            callback=self._cbEnableKeys,
                            user_data=[self.cir1, 0])#,
                        self.cirColor1 = dpg.add_color_edit(self.cbRBG[1],
                                        #callback=sa,
                                        callback=self._coloredit,
                                        user_data=[self.cir1, 1],
                                        no_alpha= True, label="Color")
                                           #callback=sa)
                        self.cirR1 = dpg.add_slider_int(label="Radius", 
                                        #callback=sa,
                                        callback=self._radii,
                                        user_data=[self.cir1, 1],
                                        max_value=self.frame_height/2, default_value = 20)
                        self.cirT1 = dpg.add_slider_int(label="Thickness", 
                                        callback=self._thickness,
                                        user_data=[self.cir1, 1],
                                        max_value=10, default_value = 2)
                        #dpg.add_same_line()
                    with dpg.collapsing_header(
                                    label="Circle 3", closable=False,
                                    default_open=True) as self.cir2:
                        self.cbEnableOffset[self.cir2] = dpg.add_checkbox(
                            label="Enable ",
                            default_value=False,
                            callback=self._cbEnableKeys,
                            user_data=[self.cir2, 0])#,
                        self.cirColor3 = dpg.add_color_edit(self.cbRBG[2],
                                        #callback=sa,
                                        callback=self._coloredit,
                                        user_data=[self.cir2, 2],
                                        no_alpha= True, label="Color")
                        self.cirR2 = dpg.add_slider_int(label="Radius", 
                                        #callback=sa,
                                        callback=self._radii,
                                        user_data=[self.cir2, 2],
                                        max_value=self.frame_height/2, default_value = 20)
                        self.cirT2 = dpg.add_slider_int(label="Thickness", 
                                        callback=self._thickness,
                                        user_data=[self.cir2, 2],
                                        max_value=10, default_value = 2)
                        #dpg.add_same_line()
                    with dpg.collapsing_header(
                                    label="Crosshair 1", closable=False,
                                    default_open=True) as self.cross1:
                        self.cbEnableOffset[self.cross1] = dpg.add_checkbox(
                            label="Enable ",
                            default_value=False,
                            callback=self._cbEnableKeys,
                            user_data=[self.cross1, 0])#,
                        self.croColor1 = dpg.add_color_edit(self.cbRBG[3],
                                        #callback=sa,
                                        callback=self._coloredit,
                                        user_data=[self.cross1, 3],
                                        no_alpha= True, label="Color")
                        self.crsL1 = dpg.add_slider_int(label="Length", 
                                        callback=self._legnth,
                                        user_data=[self.cross1, 0],
                                        max_value=self.frame_height, 
                                        default_value = self.frame_height)
                        self.crsR1 = dpg.add_slider_int(label="Angle", max_value=360,
                                        callback=self._crosshair,
                                        user_data=[self.cross1, 0],
                                        )
                        self.crsT1 = dpg.add_slider_int(label="Thickness", 
                                        callback=self._thickness,
                                        user_data=[self.cross1, 3],
                                        max_value=10, default_value = 2)
                        #dpg.add_same_line()
                    with dpg.collapsing_header(
                                    label="Crosshair 2", closable=False,
                                    default_open=True) as self.cross2:
                        self.cbEnableOffset[self.cross2] = dpg.add_checkbox(
                            label="Enable ",
                            default_value=False,
                            callback=self._cbEnableKeys,
                            user_data=[self.cross2, 0])#,
                        self.croColor2 = dpg.add_color_edit(self.cbRBG[4],
                                        callback=self._coloredit,
                                        user_data=[self.cross2, 4],
                                        no_alpha= True, label="Color")
                        self.crsL2 = dpg.add_slider_int(label="Length", 
                                        callback=self._legnth,
                                        user_data=[self.cross2, 1],
                                        max_value=self.frame_height, 
                                        default_value = self.frame_height)
                        self.crsR2 = dpg.add_slider_int(label="Angle", 
                                        callback=self._crosshair,
                                        user_data=[self.cross2, 1],
                                        max_value=360)
                        self.crsT2 = dpg.add_slider_int(label="Thickness", 
                                        callback=self._thickness,
                                        user_data=[self.cross2, 4],
                                        max_value=10, default_value = 2)
                        #dpg.add_same_line()


                with dpg.tab(label="Camera Control") as self.cameraTab:
                    dpg.add_text("This is the tab 2!")

    def _coloredit(self, sender, app_data, user_data):
        for i in range (0, 4): app_data[i] = int(app_data[i]*255)
        if user_data[1] == 0:
            self.cbRBG[user_data[1]] = app_data
            print ("Color Circle {}:", user_data[1], self.cbRBG[user_data[1]])
        elif user_data[1] == 1:
            self.cbRBG[user_data[1]] = app_data
            print ("Color Circle {}:", user_data[1], self.cbRBG[user_data[1]])
        elif user_data[1] == 2:
            self.cbRBG[user_data[1]] = app_data
            print ("Color Circle {}:", user_data[1], self.cbRBG[user_data[1]])
        elif user_data[1] == 3:
            self.cbRBG[user_data[1]] = app_data
            print ("Color Crosshair hair {}:", user_data[1], self.cbRBG[user_data[1]])
        elif user_data[1] == 4:
            self.cbRBG[user_data[1]] = app_data
            print ("Color Crosshair {}:", user_data[1], self.cbRBG[user_data[1]])

    def _legnth(self, sender, app_data, user_data):
        if user_data[1] == 0:
            self.cbLength[user_data[1]] = dpg.get_value(self.crsL1)
            print ("Thickness Cross hair {}:", user_data[1], self.cbLength[user_data[1]])
        elif user_data[1] == 1:
            self.cbLength[user_data[1]] = dpg.get_value(self.crsL2)
            print ("Thickness Cross hair {}:", user_data[1], self.cbLength[user_data[1]])

    def _radii(self, sender, app_data, user_data):
        if user_data[1] == 0:
            self.cbRadius[user_data[1]] = dpg.get_value(self.cirR0)
            print ("Circle Radius {}:", user_data[1], self.cbRadius[user_data[1]])
        elif user_data[1] == 1:
            self.cbRadius[user_data[1]] = dpg.get_value(self.cirR1)
            print ("Circle Radius {}:", user_data[1], self.cbRadius[user_data[1]])
        elif user_data[1] == 2:
            self.cbRadius[user_data[1]] = dpg.get_value(self.cirR2)
            print ("Circle Radius {}:", user_data[1], self.cbRadius[user_data[1]])

    def _thickness(self, sender, app_data, user_data):
        if user_data[1] == 0:
            self.cbThickness[user_data[1]] = dpg.get_value(self.cirT0)
            print ("Thickness Cross hair {}:", user_data[1], self.cbThickness[user_data[1]])
        elif user_data[1] == 1:
            self.cbThickness[user_data[1]] = dpg.get_value(self.cirT1)
            print ("Thickness Cross hair {}:", user_data[1], self.cbThickness[user_data[1]])
        elif user_data[1] == 2:
            self.cbThickness[user_data[1]] = dpg.get_value(self.cirT2)
            print ("Thickness Cross hair {}:", user_data[1], self.cbThickness[user_data[1]])
        elif user_data[1] == 3:
            self.cbThickness[user_data[1]] = dpg.get_value(self.crsT1)
            print ("Thickness Cross hair {}:", user_data[1], self.cbThickness[user_data[1]])
        elif user_data[1] == 4:
            self.cbThickness[user_data[1]] = dpg.get_value(self.crsT2)
            print ("Thickness Cross hair {}:", user_data[1], self.cbThickness[user_data[1]])

    def _crosshair(self, sender, app_data, user_data):
        if user_data[1] == 0:
            self.cbAngle[user_data[1]] = dpg.get_value(self.crsR1)
            print ("Angle Cross hair {}:", user_data[1], self.cbAngle[user_data[1]])
        elif user_data[1] == 1:
            self.cbAngle[user_data[1]] = dpg.get_value(self.crsR2)
            print ("Angle Cross hair {}:", user_data[1], self.cbAngle[user_data[1]])

    def _centre_position(self, sender, app_data, user_data):
        if user_data[1] == 0:
            self.xoffset = int(self.frame_width/2)
            self.yoffset = int(self.frame_height/2)
            dpg.set_value(self.cpoY, self.yoffset)
            dpg.set_value(self.cpoX, self.xoffset)
            print ("centering offset:", self.xoffset, self.yoffset)
        elif user_data[1] == 1:
            self.yoffset = int(dpg.get_value(self.cpoY))
            print ("y offset:", self.yoffset)
        elif user_data[1] == 2:
            self.xoffset = int(dpg.get_value(self.cpoX))
            print ("x offset:", self.xoffset)

    def _cbEnableKeys(self, sender, app_data, user_data):
        with dpg.mutex():
            if user_data[0] == self.cpo:
                self.cbOffset = dpg.get_value(
                    self.cbEnableOffset[user_data[0]])
                print("Enable offset: {}".format(self.cbOffset))
            elif user_data[0] == self.cross1:
                self.cbCrossEnable[0] = dpg.get_value(
                    self.cbEnableOffset[user_data[0]])
                print("Enable crosshair 1: {}".format(self.cbCrossEnable[0]))
            elif user_data[0] == self.cross2:
                self.cbCrossEnable[1] = dpg.get_value(
                    self.cbEnableOffset[user_data[0]])
                print("Enable crosshair 2: {}".format(self.cbCrossEnable[1]))
            elif user_data[0] == self.cir2:
                self.cbCircleEnable[2] = dpg.get_value(
                    self.cbEnableOffset[user_data[0]])
                print("Enable cbCircleEnable 2: {}".format(self.cbCircleEnable[2]))
            elif user_data[0] == self.cir1:
                self.cbCircleEnable[1] = dpg.get_value(
                    self.cbEnableOffset[user_data[0]])
                print("Enable cbCircleEnable 1: {}".format(self.cbCircleEnable[1]))
            elif user_data[0] == self.cir0:
                self.cbCircleEnable[0] = dpg.get_value(
                    self.cbEnableOffset[user_data[0]])
                print("Enable cbCircleEnable 0: {}".format(self.cbCircleEnable[0]))
            else:
                print("undefined ")


        pass

    def declareCalibrationVariables(self):
        self.cbCrossEnable = {}
        self.cbCrossEnable[0] = False
        self.cbCrossEnable[1] = False

        self.cbRadius = {}
        self.cbRadius[0] = 20
        self.cbRadius[1] = 20
        self.cbRadius[2] = 20

        self.cbCircleEnable = {}
        self.cbCircleEnable[0] = False
        self.cbCircleEnable[1] = False
        self.cbCircleEnable[2] = False

        self.cbAngle = {}
        self.cbAngle[0] =0 
        self.cbAngle[1] = 0

        self.cbLength = {}
        self.cbLength[0] = self.frame_height
        self.cbLength[1] = self.frame_height

        self.cbThickness = {}
        self.cbThickness[0] = 2
        self.cbThickness[1] = 2
        self.cbThickness[2] = 2
        self.cbThickness[3] = 2
        self.cbThickness[4] = 2

        self.cbRBG = {}
        self.cbRBG[0] = (102, 179,   0)
        self.cbRBG[1] = (202, 9  ,  10)
        self.cbRBG[2] = (102, 102, 179)
        self.cbRBG[3] = (1  , 1  , 230)
        self.cbRBG[4] = (102, 19 , 179)
        self.cbOffset = False

        self.xoffset = int(self.frame_width/2)
        self.yoffset = int(self.frame_height/2)
