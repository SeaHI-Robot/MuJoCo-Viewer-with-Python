"""
Description:
    Implement controller here

Auther:
    SeaHI-Robot:  https://github.com/SeaHI-Robot
    Contact_Me: seahirobot@gmail.com
    
For learning purposes only, do not spread without authorization.
"""

import mujoco as mjc
from mujoco.glfw import glfw
import os
import numpy as np

def init_controller(model,data):
    #initialize the controller here. This function is called once, in the beginning
   
    # #################### An example  ####################
    # random initial rotational velocity:
    # mjc.mj_resetData(model, data)
    # data.qvel[3:6] = 5*np.random.randn(3)
   
    pass

def controller(model, data):
    #put the controller here. This function is called inside the simulation.
    pass


