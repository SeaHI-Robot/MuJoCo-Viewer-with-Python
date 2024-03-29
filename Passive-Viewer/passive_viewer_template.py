"""
Description:
    Call mujoco passive viewer with python.
    press "space" to pause.

Auther:
    SeaHI-Robot:  https://github.com/SeaHI-Robot
    Contact_Me: seahirobot@gmail.com
    
For learning purposes only, do not spread without authorization.
"""


import mujoco
import numpy as np
# import matplotlib.pyplot as plt
# import scipy
import time
import mujoco.viewer


model = mujoco.MjModel.from_xml_path("../models/humanoid.xml")
data = mujoco.MjData(model)


paused = False
def key_callback(keycode):
    if chr(keycode) == ' ':
        global paused
        paused = not paused

# left_ui_pannel, right_ui_pannel are hidden here, toggle `show_left_ui` `show_right_ui` to show the pannels
with mujoco.viewer.launch_passive(model, data, key_callback=key_callback, show_left_ui=False, show_right_ui=False) as viewer:


    # viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTFORCE] = 1
    # viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = 1
    # viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_TRANSPARENT] = 1
    # viewer.cam.trackbodyid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "torso")
    # viewer.cam.distance = 3
    # trackbodyid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "<body name string>")
    # viewer.cam.type = mujoco.mjtCamera.mjCAMERA_TRACKING
    # viewer.cam.trackbodyid = trackbodyid


    # # tweak scales of contact visualization elements
    # model.vis.scale.contactwidth = 0.2
    # model.vis.scale.contactheight = 0.03
    # model.vis.scale.forcewidth = 0.05
    # # Set the scale of visualized contact forces to 1cm/N.
    # model.vis.map.force = 0.01



    # while viewer.is_running() and time.time() - start < 30:
    while viewer.is_running():
        step_start = time.time()

        # mj_step can be replaced with code that also evaluates
        # a policy and applies a control signal before stepping the physics.
        if not paused:
            viewer.cam.lookat = data.body('torso').subtree_com
            mujoco.mj_step(model, data)


        # Pick up changes to the physics state, apply perturbations, update options from GUI.
        viewer.sync()

        # Rudimentary time keeping, will drift relative to wall clock.
        time_until_next_step = model.opt.timestep - (time.time() - step_start)
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)

