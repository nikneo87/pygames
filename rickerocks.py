# Nikhil Ninan - 2013
# Requires codeskulptor platform to run
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
SHIP_ANG_VEL = (2*math.pi*3.5/360)
SHIP_ACC_VEC_SCALE = 0.15
SHIP_FRICTION_COEFF = 0.99
MISSILE_VEL_MUL = 6

started = False
missile_group = set([])
rock_group = set([])
explosion_group = set([])

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
#soundtrack is a preview of a track owned and created by Ronald Jenkees. I do not own this track. Do not redistribute
soundtrack = simplegui.load_sound("http://dc126.4shared.com/img/449393146/8d270f02/dlink__2Fdownload_2F8d0YPiWd_3Ftsid_3D20130608-54853-88dc3ac0/preview.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.ogg")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            ship_img_center = [self.image_center[0]+self.image_size[0], self.image_center[1]]
        else:
            ship_img_center = self.image_center
        canvas.draw_image(self.image, ship_img_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        fwd_vec = angle_to_vector(self.angle)
        for dim in range(2):
            self.vel[dim] *= SHIP_FRICTION_COEFF
            if self.thrust:
                self.vel[dim] += SHIP_ACC_VEC_SCALE*fwd_vec[dim]
            self.pos[dim] += self.vel[dim]
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        self.angle += self.angle_vel
        
    def set_thrust(self, isOn):
        self.thrust = isOn
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
        
    def set_ang_vel(self, ang_vel):
        self.angle_vel = ang_vel
        
    def shoot(self):
        missile_pos = list(my_ship.pos)
        missile_angle = my_ship.angle
        fwd_vec = angle_to_vector(missile_angle)
        missile_vel = list(my_ship.vel)
        for dim in range(2):
            missile_pos[dim] += (my_ship.image_size[dim]/2)*fwd_vec[dim]
            missile_vel[dim] += MISSILE_VEL_MUL*fwd_vec[dim]
        a_missile = Sprite(missile_pos, missile_vel, missile_angle, 0, missile_image, missile_info, missile_sound)    
        missile_group.add(a_missile)
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if (self.animated):
            imgcenter = [self.image_center[0]+(self.age*self.image_size[0]), self.image_center[1]]
        else:
            imgcenter = self.image_center 
        canvas.draw_image(self.image, imgcenter, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        for dim in range(2):
            self.pos[dim] += self.vel[dim]
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        self.angle += self.angle_vel 
        self.age += 1
        if (self.age >= self.lifespan):
            return True
        else:
            return False
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object): 
        distance = dist(self.get_position(), other_object.get_position())
        rad_sum = self.get_radius() + other_object.get_radius()
        if (distance <= rad_sum):
            return True
        else:
            return False
           
def draw(canvas):
    global time, score, lives, started, rock_group, missile_group, explosion_group
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])
     
    canvas.draw_text("Score", [WIDTH-100,30], 30,"White")
    canvas.draw_text("Lives", [5,30], 30,"White")
    canvas.draw_text(str(score), [WIDTH-100,60], 30,"White")
    canvas.draw_text(str(lives), [5,60], 30,"White")
    
    if (not started):
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH/2, HEIGHT/2],splash_info.get_size())
    else:
        # update ship and sprites
        my_ship.draw(canvas)
        my_ship.update()
        process_sprite_group(canvas, rock_group)
        process_sprite_group(canvas, missile_group)
        process_sprite_group(canvas, explosion_group)
            
        lives_lost = group_collide(rock_group, my_ship)
        score_gained = group_group_collide(missile_group, rock_group)
        lives -= lives_lost
        score += score_gained
        if (lives <= 0):
            started = False
            rock_group = set([])
            missile_group = set([])
            explosion_group = set([])
            timer.stop()
            soundtrack.rewind()
            
# timer handler that spawns a rock    
def rock_spawner():
    global score
    r_pos = [random.random()*WIDTH, random.random()*HEIGHT]
    if (score > 50):
        max_vel = 2.5
    else:
        max_vel = 1.5    
    r_vel = [(random.random()*max_vel*2)-max_vel, (random.random()*max_vel*2)-max_vel]
    max_avel = SHIP_ANG_VEL*2
    r_avel = (random.random()*max_avel*2)-max_avel
    a_rock = Sprite(r_pos, r_vel, 0, r_avel, asteroid_image, asteroid_info)
    if len(rock_group) < 12 :
        if(dist(a_rock.get_position(), my_ship.get_position()) >= 100):
            rock_group.add(a_rock)

def process_sprite_group(canvas, sprite_set):
    for sprite in list(sprite_set):
        sprite.draw(canvas)
        kill = sprite.update()
        if kill:
            sprite_set.remove(sprite)
        
def group_collide(group, other_object):
    collision_count = 0
    for sprite in list(group):
        if sprite.collide(other_object):
            collision_count += 1
            ex_sprite = Sprite(sprite.get_position(), sprite.vel, 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(ex_sprite)
            group.remove(sprite)
    return collision_count
         
def group_group_collide(groupa, groupb):
    collisions = 0 
    for groupa_obj in list(groupa):
        t_collisions = group_collide(groupb, groupa_obj)
        if (t_collisions > 0):
            groupa.remove(groupa_obj)
            collisions += t_collisions
    return collisions
    
    
def down(key):
    if key == simplegui.KEY_MAP["right"]:
        my_ship.set_ang_vel(SHIP_ANG_VEL)
    if key == simplegui.KEY_MAP["left"]:
        my_ship.set_ang_vel(-SHIP_ANG_VEL)
    if key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(True)
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        
def up(key):
    if (key == simplegui.KEY_MAP["right"] or key == simplegui.KEY_MAP["left"]):
        my_ship.set_ang_vel(0)
    if key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(False)

def click(click_pos):
    global score, lives, started
    if (not started):
        x_left = (WIDTH/2) - (((splash_info.get_size())[0])/2)
        x_right = (WIDTH/2) + (((splash_info.get_size())[0])/2)
        y_top = (HEIGHT/2) - (((splash_info.get_size())[1])/2)
        y_bot = (HEIGHT/2) + (((splash_info.get_size())[1])/2)
        if ((click_pos[0] >= x_left) and (click_pos[0] <= x_right) and (click_pos[1] >= y_top) and (click_pos[1] <= y_bot)):
            score = 0
            lives = 3
            timer.start()
            soundtrack.play()
            started = True
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1.5, -1], 0, SHIP_ANG_VEL*-2, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(down)
frame.set_keyup_handler(up)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
frame.start()