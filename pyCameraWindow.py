#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dearpygui.dearpygui as dpg
import numpy as np
import cv2 as cv
import operator


class CameraWindow():
    def __init__(self, cc):
        self.cc = cc

        ret, frame = cc.vid.read()

        data = np.flip(frame, 2)  # because the camera data comes in as BGR and we need RGB
        data = data.ravel()  # flatten camera data to a 1 d stricture
        data = np.asfarray(data, dtype='f')  # change data type to 32bit floats
        self.texture_data = np.true_divide(data, 255.0)  # normalize image data to prepare for GPU

        print("texture_data Array:")
        print("Array is of type: ", type(self.texture_data))
        print("No. of dimensions: ", self.texture_data.ndim)
        print("Shape of array: ", self.texture_data.shape)
        print("Size of array: ", self.texture_data.size)
        print("Array stores elements of type: ", self.texture_data.dtype)

        with dpg.texture_registry(show=True):
            dpg.add_raw_texture(frame.shape[1], frame.shape[0], self.texture_data, tag="texture_tag", format=dpg.mvFormat_Float_rgb)
        
        with dpg.window(label="Capture Window",pos=(500, 0),
                        no_close=True) as self.mainForm:
            dpg.add_image("texture_tag")


    def rotate(self, p, origin=(0, 0), degrees=0):
        angle = np.deg2rad(degrees)
        R = np.array([[np.cos(angle), -np.sin(angle)],
                      [np.sin(angle),  np.cos(angle)]])
        o = np.atleast_2d(origin)
        p = np.atleast_2d(p)
        return np.squeeze((R @ (p.T-o.T) + o.T).T)
    
    

    def update_frame(self):

        # updating the texture in a while loop the frame rate will be limited to the camera frame rate.
        # commenting out the "ret, frame = vid.read()" line will show the full speed that operations and updating a texture can run at
        
        ret, frame = self.cc.vid.read()
        cc = self.cc
        for i in range(0, 3):
            if cc.cbCircleEnable[i] is True:
                j = 1
                cv.circle(frame, (int(cc.xoffset), int(cc.yoffset)), 
                          radius = cc.cbRadius[i], 
                          color = (cc.cbRBG[i][2]*j, cc.cbRBG[i][1]*j, cc.cbRBG[i][0]*j), 
                          thickness = cc.cbThickness[i])
        for i in range(0, 2):
            if cc.cbCrossEnable[i] is True:
                j = 1
                origin = (cc.xoffset, cc.yoffset)
                points = [(int(cc.xoffset - cc.cbLength[i]/2 ), int(cc.yoffset)),
                          (int(cc.xoffset + cc.cbLength[i]/2 ), int(cc.yoffset))]
                rp = self.rotate(points, origin=origin, degrees=cc.cbAngle[i])
                cv.line(frame, (int(rp[0][0] ), int(rp[0][1])), 
                          (int(rp[1][0] ), int(rp[1][1])), 
                          color = (cc.cbRBG[i+3][2]*j, cc.cbRBG[i+3][1]*j, cc.cbRBG[i+3][0]*j), 
                          thickness = cc.cbThickness[i+3])
                points = [(int(cc.xoffset), int(cc.yoffset - cc.cbLength[i]/2)),
                          (int(cc.xoffset), int(cc.yoffset + cc.cbLength[i]/2))]
                rp = self.rotate(points, origin=origin, degrees=cc.cbAngle[i])
                cv.line(frame, (int(rp[0][0] ), int(rp[0][1])), 
                          (int(rp[1][0] ), int(rp[1][1])), 
                          color = (cc.cbRBG[i+3][2]*j, cc.cbRBG[i+3][1]*j, cc.cbRBG[i+3][0]*j), 
                          thickness = cc.cbThickness[i+3])
        

        data = np.flip(frame, 2)
        data = data.ravel()
        data = np.asfarray(data, dtype='f')
        self.texture_data = np.true_divide(data, 255.0)
        dpg.set_value("texture_tag", self.texture_data)

        # to compare to the base example in the open cv tutorials uncomment below
        #cv.imshow('frame', frame)

