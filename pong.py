# Nikhil Ninan - 2013
# requires codeskulptor platform to run

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [random.randrange(2,4),-(random.randrange(1,3))]
    if(not right):
        ball_vel[0] = -ball_vel[0] 
# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    paddle1_vel = 0
    paddle2_vel = 0
    paddle1_pos = (HEIGHT/2) - HALF_PAD_HEIGHT
    paddle2_pos = (HEIGHT/2) - HALF_PAD_HEIGHT
    ball_init(True)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    scolor = []
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos = paddle1_pos if ((paddle1_pos + paddle1_vel <= 0) or (paddle1_pos + paddle1_vel >= HEIGHT - 1 - PAD_HEIGHT)) else (paddle1_pos + paddle1_vel)
    paddle2_pos = paddle2_pos if ((paddle2_pos + paddle2_vel <= 0) or (paddle2_pos + paddle2_vel >= HEIGHT - 1 - PAD_HEIGHT)) else (paddle2_pos + paddle2_vel)
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_polygon([[0,paddle1_pos],[PAD_WIDTH,paddle1_pos],[PAD_WIDTH,(paddle1_pos + PAD_HEIGHT)],[0, (paddle1_pos + PAD_HEIGHT)]], 1, "White", "Green")
    c.draw_polygon([[(WIDTH),paddle2_pos],[(WIDTH),(paddle2_pos + PAD_HEIGHT)],[(WIDTH - PAD_WIDTH),(paddle2_pos + PAD_HEIGHT)],[(WIDTH - PAD_WIDTH), paddle2_pos]], 1, "Yellow", "Blue")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #top/bottom collision
    if((ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= HEIGHT - 1 - BALL_RADIUS)):
        ball_vel[1] = -ball_vel[1]
        
    #gutter/paddle collision
    if(ball_pos[0] <= PAD_WIDTH + BALL_RADIUS):
        if((ball_pos[1] >= paddle1_pos) and (ball_pos[1] <= paddle1_pos + PAD_HEIGHT)):
            ball_vel[0] = -(1.1 * ball_vel[0])
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score2 += 1
            ball_init(True)
    if(ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS):
        if((ball_pos[1] >= paddle2_pos) and (ball_pos[1] <= paddle2_pos + PAD_HEIGHT)):
            ball_vel[0] = -(1.1 * ball_vel[0])
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score1 += 1
            ball_init(False)
            
    # draw ball and scores
    if(score1 > score2):
        scolor = ["Green", "Red"]
    elif(score1 < score2):
        scolor = ["Red", "Green"]
    else:
        scolor = ["Green", "Green"]
    c.draw_text(str(score1), [WIDTH/4,HEIGHT/4], 50, scolor[0])
    c.draw_text(str(score2), [3*WIDTH/4,HEIGHT/4], 50, scolor[1])
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "Red")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if(key == simplegui.KEY_MAP["w"]):
        paddle1_vel = -4
    if(key == simplegui.KEY_MAP["s"]):
        paddle1_vel = 4
    if(key == simplegui.KEY_MAP["up"]):
        paddle2_vel = -4
    if(key == simplegui.KEY_MAP["down"]):
        paddle2_vel = 4
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if(key == simplegui.KEY_MAP["w"]):
        paddle1_vel = 0
    if(key == simplegui.KEY_MAP["s"]):
        paddle1_vel = 0
    if(key == simplegui.KEY_MAP["up"]):
        paddle2_vel = 0
    if(key == simplegui.KEY_MAP["down"]):
        paddle2_vel = 0

def click():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", click)


# start frame
frame.start()
new_game()