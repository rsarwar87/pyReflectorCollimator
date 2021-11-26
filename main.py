#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dearpygui.dearpygui as dpg

from pyCameraController import CameraController
from pyCameraWindow import CameraWindow

if __name__ == "__main__":
    cc = CameraController(3)
    dpg.create_context()
    dpg.create_viewport(title='PyReflectorCollimator', width=1800, height=800)
    dpg.setup_dearpygui()

    cc.create_window()

    cw = CameraWindow(cc)
    print ("Initialized")


    dpg.show_metrics()
    dpg.show_viewport()
    while dpg.is_dearpygui_running():
        cw.update_frame()
        dpg.render_dearpygui_frame()
    


    cc.vid.release()
    #cv.destroyAllWindows() # when using upen cv window "imshow" call this also
    dpg.destroy_context()

