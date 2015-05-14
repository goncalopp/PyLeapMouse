#William Yager
#Leap Python mouse controller POC
import sys
from leap import Leap, Mouse
from PalmControl import Palm_Control_Listener  #For palm-tilt based control
from FingerControl import Finger_Control_Listener  #For finger-pointing control
from MotionControl import Motion_Control_Listener  #For motion control
from TouchControl import TouchControlListener
import time

def show_help():
    print "----------------------------------PyLeapMouse----------------------------------"
    print "Use --finger (or blank) for pointer finger control, and --palm for palm control."
    print "Set smooth aggressiveness (# samples) with \"--smooth-aggressiveness [# samples]\""
    print "Set smooth falloff with \"--smooth-falloff [% per sample]\""
    print "Read README.md for even more info.\n"

def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        show_help()
        return

    print "----------------------------------PyLeapMouse----------------------------------"
    print "Use --finger (or blank) for pointer finger control, and --palm for palm control."
    print "Use -h or --help for more info.\n"

    #Default
    mode= 'finger'
    smooth_aggressiveness = 8
    smooth_falloff = 1.3

    for i in range(0,len(sys.argv)):
        arg = sys.argv[i].lower()
        if "--palm" in arg:
            mode='palm'
        if "--motion" in arg:
            mode='motion'
        if "--touch" in arg:
            mode= 'touch'
        if "--smooth-falloff" in arg:
            smooth_falloff = float(sys.argv[i+1])
        if "--smooth-aggressiveness" in arg:
            smooth_aggressiveness = int(sys.argv[i+1])


    controller = Leap.Controller()  #Get a Leap controller
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    #Create a custom listener object which controls the mouse
    listener = None;  #I'm tired and can't think of a way to organize this segment nicely
    print "Using {} mode...".format( mode )
    if mode == 'finger':  #Finger pointer mode
        listener = Finger_Control_Listener(Mouse, smooth_aggressiveness=smooth_aggressiveness, smooth_falloff=smooth_falloff)
    elif mode == 'palm':  #Palm control mode
        listener = Palm_Control_Listener(Mouse)
    elif mode == 'motion':  #Motion control mode
        listener = Motion_Control_Listener(Mouse)
    elif mode == 'touch':  #Touchscreen mode
        listener= TouchControlListener( controller )

    print "Adding Listener."
    controller.add_listener(listener)  #Attach the listener

    #Keep this process running until Ctrl-C is pressed
    print "Press Ctrl-C to quit..."
    try:
        while True:
            listener.tap_listener.g.draw()
            time.sleep(0.5)
    except KeyboardInterrupt:
        return
    finally:
        #Remove the sample listener when done
        controller.remove_listener(listener)

main()
