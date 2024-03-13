"""
Description:
    The main script

Auther:
    SeaHI-Robot:  https://github.com/SeaHI-Robot
    Contact_Me: seahirobot@gmail.com
    
For learning purposes only, do not spread without authorization.
"""


from controller_implement import *


############################## Edit This ! ##############################

# xml_path = '../models/ur5e/scene.xml' #xml file
# xml_path = '../models/hello.xml' #xml file
xml_path = '../models/free_body.xml' #xml file

simend = 10 #simulation time

############################## Edit This ! ##############################



if __name__ == "__main__":


    def keyboard(window, key, scancode, act, mods):
        if act == glfw.PRESS and key == glfw.KEY_BACKSPACE:
            mjc.mj_resetData(model, data)
            mjc.mj_forward(model, data)

    def mouse_button(window, button, act, mods):
        # update button state
        global button_left
        global button_middle
        global button_right

        button_left = (glfw.get_mouse_button(
            window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS)
        button_middle = (glfw.get_mouse_button(
            window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS)
        button_right = (glfw.get_mouse_button(
            window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS)

        # update mouse position
        glfw.get_cursor_pos(window)

    def mouse_move(window, xpos, ypos):
        # compute mouse displacement, save
        global lastx
        global lasty
        global button_left
        global button_middle
        global button_right

        dx = xpos - lastx
        dy = ypos - lasty
        lastx = xpos
        lasty = ypos

        # no buttons down: nothing to do
        if (not button_left) and (not button_middle) and (not button_right):
            return

        # get current window size
        width, height = glfw.get_window_size(window)

        # get shift key state
        PRESS_LEFT_SHIFT = glfw.get_key(
            window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
        PRESS_RIGHT_SHIFT = glfw.get_key(
            window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS
        mod_shift = (PRESS_LEFT_SHIFT or PRESS_RIGHT_SHIFT)

        # determine action based on mouse button
        if button_right:
            if mod_shift:
                action = mjc.mjtMouse.mjMOUSE_MOVE_H
            else:
                action = mjc.mjtMouse.mjMOUSE_MOVE_V
        elif button_left:
            if mod_shift:
                action = mjc.mjtMouse.mjMOUSE_ROTATE_H
            else:
                action = mjc.mjtMouse.mjMOUSE_ROTATE_V
        else:
            action = mjc.mjtMouse.mjMOUSE_ZOOM

        mjc.mjv_moveCamera(model, action, dx/height,
                        dy/height, scene, cam)

    def scroll(window, xoffset, yoffset):
        action = mjc.mjtMouse.mjMOUSE_ZOOM
        mjc.mjv_moveCamera(model, action, 0.0, -0.05 *
                        yoffset, scene, cam)

##############################################################################################
        
    print_camera_config = 1 #set to 1 to print camera config
                            #this is useful for initializing view of the model)
    
    # For callback functions
    button_left = False
    button_middle = False
    button_right = False
    lastx = 0
    lasty = 0
    
    #get the full path
    dirname = os.path.dirname(__file__)
    abspath = os.path.join(dirname + "/" + xml_path)
    xml_path = abspath

    # MuJoCo data structures
    model = mjc.MjModel.from_xml_path(xml_path)  # MuJoCo model
    data = mjc.MjData(model)                # MuJoCo data
    cam = mjc.MjvCamera()                        # Abstract camera
    opt = mjc.MjvOption()                        # visualization options

    # Init GLFW, create window, make OpenGL context current, request v-sync
    glfw.init()
    window = glfw.create_window(900, 600, "MuJoCo GLFW Viewer", None, None)
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    # initialize visualization data structures
    mjc.mjv_defaultCamera(cam)
    mjc.mjv_defaultOption(opt)
    scene = mjc.MjvScene(model, maxgeom=10000)
    context = mjc.MjrContext(model, mjc.mjtFontScale.mjFONTSCALE_150.value)


    #################### Visualize Contact ####################
    # # visualize contact frames and forces, make body transparent
    # mjc.mjv_defaultOption(opt)
    # opt.flags[mjc.mjtVisFlag.mjVIS_CONTACTPOINT] = True
    # opt.flags[mjc.mjtVisFlag.mjVIS_CONTACTFORCE] = True
    # opt.flags[mjc.mjtVisFlag.mjVIS_TRANSPARENT] = True
    # # tweak scales of contact visualization elements
    # model.vis.scale.contactwidth = 0.1
    # model.vis.scale.contactheight = 0.03
    # model.vis.scale.forcewidth = 0.05
    # model.vis.map.force = 0.3
    #################### Visualize Contact ####################


    #################### Init Camera View Config ####################
    # Example on how to set camera configuration
    cam.azimuth = -125
    cam.elevation = -11.43
    cam.distance = 1.7
    cam.lookat = np.array([-0.01, 0.06, 0.00])
    #################### Init Camera View Config ####################


    # install GLFW mouse and keyboard callbacks
    glfw.set_key_callback(window, keyboard)
    glfw.set_cursor_pos_callback(window, mouse_move)
    glfw.set_mouse_button_callback(window, mouse_button)
    glfw.set_scroll_callback(window, scroll)

    # initialize the controller
    init_controller(model,data)

    # set the controller
    mjc.set_mjcb_control(controller)


    # sim loop 
    while not glfw.window_should_close(window):
        time_prev = data.time

        while (data.time - time_prev < 1.0/60.0):
            mjc.mj_step(model, data)

        if (data.time>=simend):
            break;

        # get framebuffer viewport
        viewport_width, viewport_height = glfw.get_framebuffer_size(
            window)
        viewport = mjc.MjrRect(0, 0, viewport_width, viewport_height)

        #################### Print Camera View Config in Terminal ####################
        # print camera configuration (help to initialize the view)
        # print('cam.azimuth =',cam.azimuth,';','cam.elevation =',cam.elevation,';','cam.distance = ',cam.distance)
        # print('cam.lookat =np.array([',cam.lookat[0],',',cam.lookat[1],',',cam.lookat[2],'])')
        #################### Print Camera View Config in Terminal ####################


        # Update scene and render
        mjc.mjv_updateScene(model, data, opt, None, cam,
                        mjc.mjtCatBit.mjCAT_ALL.value, scene)
        mjc.mjr_render(viewport, scene, context)

        # swap OpenGL buffers (blocking call due to v-sync)
        glfw.swap_buffers(window)

        # process pending GUI events, call GLFW callbacks
        glfw.poll_events()

    glfw.terminate()
