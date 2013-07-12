# Nikhil Ninan - 2013
# requires codeskulptor platform to run

import simplegui
import random


# helper function to initialize globals
def init():
    global cards, exposed, state, clicks, turns
    cards = range(8)
    cards.extend(range(8))
    random.shuffle(cards)
    exposed = []
    clicks = []
    state = 0
    turns = 0
    label.set_text("Moves = "+str(turns))
    for i in range(16):
        exposed.append(False)
        
def state_machine(clk_cd_idx):
    global state, clicks, cards, exposed, turns
    #state 0 is init. 1 is single click. 2 is 2 clicks
    if(state == 0):
        state = 1
        clicks.append(clk_cd_idx)
        exposed[clk_cd_idx] = True
    elif(state == 1):
        if(not exposed[clk_cd_idx]):
            state = 2
            clicks.append(clk_cd_idx)
            exposed[clk_cd_idx] = True
            turns += 1
            label.set_text("Moves = "+str(turns))
    else:
        if(not exposed[clk_cd_idx]):
            if(cards[clicks[0]] != cards[clicks[1]]):
                #not match
                exposed[clicks[0]] = False
                exposed[clicks[1]] = False
            clicks = [clk_cd_idx]
            exposed[clk_cd_idx] = True
            state = 1
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    clk_cd_idx = pos[0]//50
    state_machine(clk_cd_idx)
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    card_pos = [15,65]
    i = 0
    for card in cards:
        displacement = 50 * i
        if (exposed[i]):
            canvas.draw_text(str(card),card_pos, 40, "Yellow")
        else:
            canvas.draw_polygon([[displacement,0],[(displacement+50),0],[(displacement+50),100],[displacement,100]],1,"Blue","Green")
            canvas.draw_text("?",card_pos, 40, "Red")
        i += 1
        card_pos[0] += 50


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
