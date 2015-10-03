# example script for using PyGaze

# # # # #
# importing the relevant libraries
import random
import constants
from pygaze import libscreen
from pygaze import libtime
from pygaze import liblog
from pygaze import libinput
from pygaze import eyetracker

# # # # #
# experiment setup

# start timing
libtime.expstart()

# create display object
disp = libscreen.Display()

# create eyetracker object
tracker = eyetracker.EyeTracker(disp)

# create keyboard object
keyboard = libinput.Keyboard(keylist=['space'], timeout=None)

# create logfile object
log = liblog.Logfile()
log.write(["trialnr", "trialtype", "endpos", "latency", "correct"])

# create screens
inscreen = libscreen.Screen()
inscreen.draw_text(text="When you see a cross, look at it and press space. Then make an eye movement to the black circle when it appears.\n\n(press space to start)", fontsize=24)
fixscreen = libscreen.Screen()
fixscreen.draw_fixation(fixtype='cross',pw=3)
targetscreens = {}
targetscreens['left'] = libscreen.Screen()
targetscreens['left'].draw_circle(pos=(int(constants.DISPSIZE[0]*0.25),constants.DISPSIZE[1]/2), fill=True)
targetscreens['right'] = libscreen.Screen()
targetscreens['right'].draw_circle(pos=(int(constants.DISPSIZE[0]*0.75),constants.DISPSIZE[1]/2), fill=True)
feedbackscreens = {}
feedbackscreens[1] = libscreen.Screen()
feedbackscreens[1].draw_text(text='correct', colour=(0,255,0), fontsize=24)
feedbackscreens[0] = libscreen.Screen()
feedbackscreens[0].draw_text(text='incorrect', colour=(255,0,0), fontsize=24)

# # # # #
# run the experiment

# calibrate eye tracker
tracker.calibrate()

# show instructions
disp.fill(inscreen)
disp.show()
keyboard.get_key()

# run 20 trials
for trialnr in range(1,21):
    # prepare trial
    trialtype = random.choice(['left','right'])
    
    # drift correction
    checked = False
    while not checked:
        disp.fill(fixscreen)
        disp.show()
        checked = tracker.drift_correction()
    
    # start eye tracking
    tracker.start_recording()
    tracker.status_msg("trial %d" % trialnr)
    tracker.log("start_trial %d trialtype %s" % (trialnr, trialtype))
    
    # present fixation
    disp.fill(screen=fixscreen)
    disp.show()
    tracker.log("fixation")
    libtime.pause(random.randint(750, 1250))
    
    # present target
    disp.fill(targetscreens[trialtype])
    t0 = disp.show()
    tracker.log("target %s" % trialtype)
    
    # wait for eye movement
    t1, startpos = tracker.wait_for_saccade_start()
    endtime, startpos, endpos = tracker.wait_for_saccade_end()
    
    # stop eye tracking
    tracker.stop_recording()
    
    # process input:
    if (trialtype == 'left' and endpos[0] < constants.DISPSIZE[0]/2) or (trialtype == 'right' and endpos[0] > constants.DISPSIZE[0]/2):
        correct = 1
    else:
        correct = 0
    
    # present feedback
    disp.fill(feedbackscreens[correct])
    disp.show()
    libtime.pause(500)
    
    # log stuff
    log.write([trialnr, trialtype, endpos, t1-t0, correct])

# end the experiment
log.close()
tracker.close()
disp.close()
libtime.expend()
