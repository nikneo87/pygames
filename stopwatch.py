# Nikhil Ninan - 2013
# requires codeskulptor platform to run

import simplegui

# define global variables
count = 0
attempts = 0
wins = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    #get mins
    mins = t//600
    remainder = t%600
    a = str(mins)
    #get seconds
    seconds = remainder//10
    bc = str(seconds)
    if(seconds < 10):
        bc = "0" + bc
    remainder %= 10
    d = str(remainder)
    return a+":"+bc+"."+d
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_time():
    if (~timer.is_running()):
        timer.start()
        
def stop_time():
    global attempts, wins
    if(timer.is_running()):
        attempts += 1
        if ((count % 10) == 0):
            wins += 1
        timer.stop()
        
def reset_time():
    global count, attempts, wins
    if(timer.is_running()):
        timer.stop()
    count = 0
    attempts = 0
    wins = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global count
    count += 1

# define draw handler
def draw(canvas):
    display = format(count)
    score = str(wins)+"/"+str(attempts)
    canvas.draw_text(display, [110,110], 35, "White")
    canvas.draw_text(score, [233,30], 30, "Green")
    
# create frame
frame = simplegui.create_frame("Stop Watch",300,200)

# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, tick)
bstart = frame.add_button("Start", start_time,100)
bstop = frame.add_button("Stop", stop_time,100)
breset = frame.add_button("Reset", reset_time,100)

# start frame
frame.start()

