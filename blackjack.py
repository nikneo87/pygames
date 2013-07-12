# Nikhil Ninan - 2013
# requires codeskulptor platform to run

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
dealt = False
outcome = "New Deal?"
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        cardstr = "Hand contains "
        for card in self.cards:
            cardstr += str(card) + " "
        return cardstr

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        has_ace = 0
        for card in self.cards:
            has_ace = 1 if (card.get_rank() == 'A') else has_ace
            value += VALUES[card.get_rank()]
        if ((has_ace == 1) and (value < 12)):
            value += 10
        return value
        
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                    self.cards.append(Card(suit, rank))

    def shuffle(self):
        # add cards back to deck and shuffle
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def __str__(self):
        deckstr = "Deck contains "
        for card in self.cards:
            deckstr += str(card) + " "
        return deckstr



#define event handlers for buttons
def deal():
    global outcome, in_play, gdeck, dhand, phand, dealt, score

    # your code goes here
    if in_play:
        score -= 1
        outcome = "Player lost. New Deal?"
        in_play = False
    else:
        in_play = True
        outcome = "Hit or Stand?"
        gdeck = Deck()
        dhand = Hand()
        phand = Hand()
        gdeck.shuffle()
        phand.add_card(gdeck.deal_card())
        phand.add_card(gdeck.deal_card())
        dhand.add_card(gdeck.deal_card())
        dhand.add_card(gdeck.deal_card())
    dealt = True

def hit():
    global in_play, outcome, score
 
    # if the hand is in play, hit the player
    if in_play:
        phand.add_card(gdeck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
        if (phand.get_value() > 21):
            outcome = "You bust. New Deal?"
            score -= 1
            in_play = False
    
def stand():
    global in_play, outcome, score
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while(dhand.get_value() < 17):
            dhand.add_card(gdeck.deal_card())
        in_play = False
        if(dhand.get_value() > 21):
            outcome = "Dealer bust! New Deal?"
            score += 1
        elif(dhand.get_value() >=  phand.get_value()):
            outcome = "Dealer wins! New Deal?"
            score -= 1
        else:
            outcome = "You win! New Deal?"
            score += 1
        # assign a message to outcome, update in_play and score
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    ppos = [10, (590 - CARD_SIZE[1])]
    dpos = [10, 5]
    prompt_pos = [210, 170]
    #canvas.draw_circle([300,300], 120, 5, "Red", "Black")
    canvas.draw_text("Blackjack", [220,310], 40, "Yellow", "serif")
    canvas.draw_text("Score: "+str(score), [10,(590 - CARD_SIZE[1] - 5)], 30, "Yellow", "serif")
    if not (in_play or (not dealt)):
        prompt_pos = [140, 170] 
    canvas.draw_text(outcome, prompt_pos, 40, "Black", "serif")
    if dealt:
        phand.draw(canvas, ppos)
        dhand.draw(canvas, dpos)
        if in_play:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [10 + CARD_BACK_CENTER[0], 5 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
frame.start()