# Nikhil Ninan - 2013

# CodeSkulptor runs in Chrome 18+, Firefox 11+, and Safari 6+.
# Some features may work in other browsers, but do not expect
# full functionality.  It does NOT run in Internet Explorer.

#INSTRUCTIONS:
#You have 2 mins to match the pattern shown at the bottom
# of the color grid. one point per correct match
# click blocks in order of pattern
#to erase move upto and including a selected block, reclick
# on that block

#optimizations to do:
# 1) create block class that will hold block cords, better than 
# 	  repeating all calculation on every refresh cycle - save battery
#     pos, circle_center becomes lookup after once only static computation - little more mem (not much)
#	  but eases up processing effort. will also improve render rate 
#  2) verify that sequence generation algorithm does not trap itself - done
# 3) see if there is a better way of doing sequence generation
# 4) create game class that keeps found_id, goal sequence, time, score, next_move list etc
# 5) dont need highlight list- should be able to use player_sequence to paint highlighted
# 6) player_sequence keeping color just for debugging - dont need this when we track found state

import simplegui
import random

WIDTH = 600
HEIGHT = 800
SEL_CIRCLE_RADIUS = 5
GRID_SIZE = 6
STOP_CLOCK = 120 #2 MINUTES TO PLAY
#generete sequence of length 5 (not too long and avoids self trapping.. 6 works too but not any higher)
SEQ_LENGTH = 5

#color map array
color_map = ["Aqua","Black","Blue", "Purple", "Fuchsia", "Red", "Silver", "Teal", "Lime", "White", "Maroon", "Olive"]
highlight_color = "Yellow"

find_id = 0
player_sequence = []
score = 0
clock = 0
time = ""
inPlay = True

#grid class
class Grid:
    def __init__(self, canvas_width, side_sqs):
        self.width = canvas_width
        self.height = canvas_width
        self.side_sqs = side_sqs
        self.sqs = side_sqs**2
        self.block_size = [self.width/side_sqs, self.height/side_sqs]
        self.grid = []
        self.highlight = []
        self.paint_grid()
        
    def paint_grid(self):
        #initialise grid painting
        #ranodm color sequence and no highlighting
        for unit in range(self.sqs):
            self.grid.append(random.randrange(0,12))
            self.highlight.append(False)
            
    def draw_block(self, canvas, pos, isHighlighted, fill_color):
        #draw a single block on the canvas
        #each block is drawn as a polygon with pos indicating
        #upper left co-ord in cartesian space
        #canvas.draw_polygon(point_list, line_width, line_color, fill_color=None)
        canvas.draw_polygon([pos, [pos[0]+self.block_size[0], pos[1]], 
                                  [pos[0]+self.block_size[0], pos[1]+self.block_size[1]], 
                                  [pos[0], pos[1]+self.block_size[1]]], 
                            1,
                            "Yellow",
                            fill_color)
        if (isHighlighted):
            #does python cast integers to bool? not sure.
            circle_center = [pos[0]+(self.block_size[0]/2), pos[1]+(self.block_size[1]/2)]
            #canvas.draw_circle(center_point, radius, line_width, line_color, fill_color=None)
            canvas.draw_circle(circle_center, SEL_CIRCLE_RADIUS, 1, "Navy", highlight_color)
            #wtf isnt this drawing a circle in Chrome?????
    
    def idx2coord(self,block_idx):
        pos_x = 0 + ((block_idx % self.side_sqs) * self.block_size[0])
        pos_y = 0 + ((block_idx // self.side_sqs) * self.block_size[1])
        return [pos_x, pos_y]
    
    def draw_grid(self, canvas):
        #draw entire grid on canvas starting from top left
        #tile blocks by pos and block_size
        for block_idx in range(self.sqs):
            #compute (x,y) coord or top left point for each block
            block_pos = self.idx2coord(block_idx)
            self.draw_block(canvas, 
                            block_pos, 
                            self.highlight[block_idx], 
                            color_map[self.grid[block_idx]])
            
    
    def click2blockidx(self, pos):
        #convert click to block index on grid
        #check that pos is within game_grid
        if ((pos[0] >= 0) and 
            (pos[0] <= self.width) and 
            (pos[1] >= 0) and
            (pos[1] <= self.width)):
            idx = (self.side_sqs * (pos[1] // self.block_size[1])) + ((pos[0] // self.block_size[0]))
        else:
            idx = None
        return idx
    
    def toggle_highlight(self, idx):
        #toggle the hightlight color for a block given its index
        if (idx != None):
            self.highlight[idx] = not self.highlight[idx]

    def get_block_color(self,idx):
        #returns color corresponding to a block index
        return color_map[self.grid[idx]]
    
# Handler for mouse click
def click(click_pos):
    global find_id, player_sequence, score
    clicked_block_idx = game_grid.click2blockidx(click_pos)
    #always match on colors not indexes since multiple solutions possible
    #index represents just one possible solution
    if ((clicked_block_idx != None) and inPlay ):
        #reject invalid clicks outside grid
        if (find_id == 0):
            #first block is special
            if (color_map[game_grid.grid[clicked_block_idx]] == color_map[game_grid.grid[goal[find_id]]]):
                #clicked color matches current goal sequence idx
                find_id += 1
                game_grid.toggle_highlight(clicked_block_idx)
                #push into player_seq in format [block_idx, block_color]
                player_sequence.append(clicked_block_idx)
        else:
            #all subsequent blocks
            #print "Player seqeunce", player_sequence #debug
            if (clicked_block_idx in player_sequence):
                #previously selected -> player wants to undo
                #undo everything upto selected block
                #dangerous to modify traversal list mid traverse - do it in a safe way
                start_idx = find_id - 1
                while (clicked_block_idx != player_sequence[start_idx]):
                    unhigh_blk_idx = player_sequence.pop()
                    game_grid.toggle_highlight(unhigh_blk_idx)
                    start_idx -= 1
                    find_id -= 1
                unhigh_blk_idx = player_sequence.pop()
                game_grid.toggle_highlight(unhigh_blk_idx)
                find_id -= 1
            else:
                #new block selection
                valid_moves = get_next_blocks(player_sequence[find_id - 1])
                #print "Valid move list: ", valid_moves
                if ((clicked_block_idx in valid_moves) 
                    and (color_map[game_grid.grid[clicked_block_idx]] == color_map[game_grid.grid[goal[find_id]]])):
                    #valid correct click - update
                    find_id += 1
                    game_grid.toggle_highlight(clicked_block_idx)
                    player_sequence.append(clicked_block_idx)
                    if(find_id == SEQ_LENGTH):
                        #found full sequence
                        score += 1
                        new_seq()

# Handler to draw on canvas
def draw(canvas):
    #draw game grid
    game_grid.draw_grid(canvas)
    connect_blocks(canvas, player_sequence, highlight_color)
    if (not inPlay):
        #reveal the missed sequence
        connect_blocks(canvas, goal, "Red")
    #draw goal sequence
    pos = [200,700]
    goal_block_size = 50
    canvas.draw_text(time,
                     [pos[0]- (2*goal_block_size + 20),(pos[1] + goal_block_size)],
                     60,
                     "White")
    for i in range(SEQ_LENGTH):
        canvas.draw_polygon([pos, [pos[0]+goal_block_size, pos[1]], 
                                  [pos[0]+goal_block_size, pos[1]+goal_block_size], 
                                  [pos[0], pos[1]+goal_block_size]], 
                            1,
                            "Yellow",
                            game_grid.get_block_color(goal[i]))
        pos[0] += goal_block_size
    #canvas.draw_text(text, point, font_size, font_color, font_face="Serrif")
    canvas.draw_text(str(score), 
                     [pos[0] + (goal_block_size),(pos[1] + goal_block_size)], 
                     60, 
                     "White")

def connect_blocks(canvas, sequence, line_color):
    #connect player sequence to enhance display of order
    term_idx = len(sequence)
    if (term_idx > 1):
        #need atleast 2 points to draw a line segment.. duh
        for idx in range(term_idx-1):
            #take each point as start and connect to immediate next
            #upto the penultimate point
            blk1 = sequence[idx]
            blk2 = sequence[idx+1]
            pos1 = game_grid.idx2coord(blk1)
            pos2 = game_grid.idx2coord(blk2)
            blk_center1 = [pos1[0]+(game_grid.block_size[0]/2), pos1[1]+(game_grid.block_size[1]/2)]
            blk_center2 = [pos2[0]+(game_grid.block_size[0]/2), pos2[1]+(game_grid.block_size[1]/2)]
            #canvas.draw_line(point1, point2, line_width, line_color)
            canvas.draw_line(blk_center1, blk_center2, 5, line_color)
            
    
#given a block, returns a list of valid next blocks
def get_next_blocks(block_idx):
    #identify given block state
    is_left = True if ((block_idx % game_grid.side_sqs) == 0) else False
    is_right = True if ((block_idx % game_grid.side_sqs) == (game_grid.side_sqs - 1)) else False
    is_top = True if ((block_idx // game_grid.side_sqs) == 0) else False
    is_bot = True if ((block_idx // game_grid.side_sqs) == (game_grid.side_sqs - 1)) else False
    #identify neighboring block indices
    block_w = block_idx - 1
    block_e = block_idx + 1
    block_n = block_idx - game_grid.side_sqs
    block_s = block_idx + game_grid.side_sqs
    block_nw = block_n - 1
    block_ne = block_n + 1
    block_sw = block_s - 1
    block_se = block_s + 1
    #assume all blocks are valid 
    next_blocks = [block_w, block_nw, block_n, block_ne, block_e, block_se, block_s, block_sw]
    #and then remove invalid ones
    if is_left:
        for bidx in [block_w, block_nw, block_sw]:
            next_blocks.remove(bidx)
    if is_right:
        for bidx in [block_e, block_ne, block_se]:
            next_blocks.remove(bidx)
    #for the next two need to check if already removed
    if is_top:
        for bidx in [block_n, block_nw, block_ne]:
            if bidx in next_blocks:
                next_blocks.remove(bidx)
    if is_bot:
        for bidx in [block_s, block_sw, block_se]:
            if bidx in next_blocks:
                next_blocks.remove(bidx)            
    return next_blocks
        
#Function to generate quest sequence    
def gen_sequence():
    #randomly pick starting block 
    start = random.randrange(0, game_grid.sqs)
    quest_sequence = [start]
    for i in range(SEQ_LENGTH - 1):
        start = quest_sequence[i]
        next_blocks = get_next_blocks(start)
        #purge already consumed blocks from next blocks list
        for sblock in quest_sequence:
            if sblock in next_blocks:
                next_blocks.remove(sblock)
        #now we have real valid next block list. randomly pick one
        quest_sequence.append(random.choice(next_blocks))
    return quest_sequence

def new_seq():
    global goal, find_id, player_sequence
    goal = gen_sequence()
    find_id = 0
    for block in player_sequence:
        game_grid.toggle_highlight(block)
    player_sequence = [] 
    #print goal #debug
    
def reset_click():
    global game_grid, score, inPlay, clock, time
    game_grid = Grid(WIDTH, GRID_SIZE)
    score = 0
    clock = 0
    time = "0:0"
    inPlay = True
    timer.start()
    #print goal #debug
    
def tick():
    #global second clock
    global clock, inPlay, time
    clock += 1
    time = str(clock//60)+":"+str(clock % 60)
    if (clock == STOP_CLOCK):
        inPlay = False
        timer.stop()
    
# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("wob", 600, 800)
timer = simplegui.create_timer(1000, tick)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
frame.add_button("Reset", reset_click)

game_grid = Grid(WIDTH, GRID_SIZE)
goal = gen_sequence()
# Start the frame animation
frame.start()
timer.start()