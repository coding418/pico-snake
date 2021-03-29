# import modules for timing, display, and random integers
import utime
from random import randint
import picodisplay as display


# picodisplay boilerplate code
width = display.get_width()
height = display.get_height()

display_buffer = bytearray(width * height * 2)
display.init(display_buffer)

backlight_intensity = 0.6
display.set_backlight(backlight_intensity)


# initialize some global variables for game
tile_size = 12 # size in pixels of square tiles
grid_w, grid_h = 20, 11 # 20*11 tiles


walls = []

def load_level(level_number):
    filename = "level-" + str(level_number) + ".txt"
    f = open(filename, "r")

    lines = f.readlines()

    y = 0

    global walls

    walls = []

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if 0 <= x < grid_w and 0 <= y < grid_h and char == '0':
                wall_pos = x, y
                walls.append(wall_pos)

        
    f.close()

score = 0
frameCount = 0

# initialize some color data
snake_color = (0, 200, 0)
food_color  = (200, 0, 0)
wall_color  = (200, 0, 200)
title_color = (255, 255, 0)
score_color = (255, 255, 255)



'''Classes: Food, SnakeNode, Snake'''
class Food:
    def __init__(self):
        self.reset_position()
        
        
    # sets new position for Food (bug: allows new position in snake...?)
    def reset_position(self):
        new_pos = randint(1, grid_w-2), randint(1, grid_h-2)
        
        global snake
        
        while snake.contains(new_pos) or check_walls(new_pos):
            new_pos = randint(1, grid_w-2), randint(1, grid_h-2)
            #print("placed food inside snake, redoing...")
            
        self.pos = new_pos


    def show(self, display):
        food_x, food_y = self.pos
    
        food_red, food_green, food_blue = food_color
        display.set_pen(food_red, food_green, food_blue)
    
        # calculate center of tile on canvas
        tile_x = (tile_size * food_x) + tile_size//2
        tile_y = (tile_size * food_y) + tile_size//2
        
        radius = (tile_size-2)//2
                
        display.circle(tile_x, tile_y, radius)





class Snake:
    def __init__(self):        
        center_of_grid = grid_w//2, grid_h//2
        self.direction = (0, 0)
        self.head = SnakeNode(center_of_grid, self.direction)
        self.length = 1
        
        
    def push(self, new_head):
        new_head.next, self.head = self.head, new_head
        self.length += 1
        
        
    def pop(self):
        current_node = self.head        
        previous_node = None
        
        num_times = 0
        
        # loop through entire list of SnakeNodes
        while current_node.next != None:
            num_times += 1
            previous_node = current_node
            current_node = current_node.next
            
        # loop ends: final node in current_node, penultimate node in previous_node
            
        #print(frameCount, self.length, num_times)
        
        # if there is a previous_node (i.e. this is not the head node)
        if previous_node != None:
            previous_node.next = None # clear pointer to final node
            self.length -= 1
        
    
    def contains(self, position):
        
        num_times = 0
        
        current_node = self.head
        
        while current_node != None:
            num_times += 1
            if current_node.pos == position:
                #print(frameCount, self.length, num_times)
                return True
            
            current_node = current_node.next
            
        #print(frameCount, self.length, num_times)
        return False
    
        
    def move(self):
        # unpack direction and position of head node
        x_dir, y_dir = self.direction        
        head_x, head_y = self.head.pos
        
        # update position according to direction
        head_x += x_dir
        head_y += y_dir
        
        # keep position within grid boundaries
        head_x %= grid_w
        head_y %= grid_h
        
        # create and return new head node
        new_head_position = head_x, head_y        
        new_node = SnakeNode(new_head_position, self.direction)
        
        return new_node


    def show(self, display):
        snake_red, snake_green, snake_blue = snake_color
        display.set_pen(snake_red, snake_green, snake_blue)
        
        current_node = self.head
        
        num_times = 0
        
        while current_node != None:    
            num_times += 1        
            if current_node != self.head:
                
                x1, y1 = current_node.pos
                x2, y2 = previous_node.pos
                
                invisible = (abs(x1-x2)>1)or(abs(y1-y2)>1)
                
                x1 *= tile_size
                y1 *= tile_size
                
                x2 *= tile_size
                y2 *= tile_size
                
                x1 += tile_size//2
                y1 += tile_size//2
                
                x2 += tile_size//2
                y2 += tile_size//2
                
                if not invisible:
                    line(x1, y1, x2, y2)
                
            else:
                # draw circle for snake head
                grid_x, grid_y = current_node.pos
            
                canvas_x = (tile_size * grid_x)
                canvas_y = (tile_size * grid_y)
                
                center_x = canvas_x+(tile_size//2)
                center_y = canvas_y+(tile_size//2)
                radius = (tile_size-4)//2
                
                display.circle(center_x, center_y, radius)
            
            previous_node = current_node
            current_node = current_node.next
        
        #print(frameCount, self.length, num_times)
        
        
    def moving(self):
        return self.direction != (0, 0)
        
        
    def check_walls(self, new_head):
        head_x, head_y = new_head.pos
        
        min_x = 0
        max_x = grid_w - 1
        
        min_y = 0
        max_y = grid_h - 1
        
        return head_x < min_x or head_x > max_x or head_y < min_y or head_y > max_y
    
    
    def check_food(self, new_head, food):
        if new_head.pos == food.pos:
            food.reset_position(self)
            
            global score
            score += 1
                      
            return True
        else:
            return False


    def update_direction(self, pressed):
        x_dir, y_dir = self.direction
        
        if pressed['A']:
            if self.direction[0] == 0:
                x_dir = -1
            y_dir = 0
                
        elif pressed['Y']:
            if self.direction[0] == 0:            
                x_dir = 1
            y_dir = 0
            
        elif pressed['B']:
            x_dir = 0
            if self.direction[1] == 0:
                y_dir = 1
            
        elif pressed['X']:
            x_dir = 0
            if self.direction[1] == 0:
                y_dir = -1
                
        self.direction = x_dir, y_dir

def check_walls(pos):
    for wall in walls:
        if pos == wall:
            return True
    
    return False
        
class SnakeNode:
    def __init__(self, position=None, direction=None, next=None, prev=None):
        self.pos = position
        self.dir = direction
        self.next = next

        
# Functions: line, debug_pattern
def line(x1, y1, x2, y2):
    start_x = min(x1, x2)
    start_y = min(y1, y2)
    
    line_thickness = 4    
    offset = line_thickness//2
        
    start_x -= offset
    start_y -= offset
    
    # for horizontal lines
    if x1 == x2:
        line_width = offset * 2
        line_height = offset + abs(y1-y2) + offset
      
    # for vertical lines
    elif y1 == y2:
        line_width = offset + abs(x1-x2) + offset
        line_height = offset * 2
    
    
    display.rectangle(start_x, start_y, line_width, line_height)


def debug_pattern():
    alternate_color = False
    
    for j in range(grid_h):        
        for i in range(grid_w):            
            if alternate_color:
                display.set_pen(0, 0, 255)
            else:
                display.set_pen(255, 0, 255)
                
            tile_x = i * tile_size
            tile_y = j * tile_size
            
            display.rectangle(tile_x, tile_y, tile_size, tile_size)
            
            alternate_color = not alternate_color
            
        alternate_color = not alternate_color
        

def update_inputs(display):
    pressed = {}
    
    pressed['A'] = display.is_pressed(display.BUTTON_A)
    pressed['B'] = display.is_pressed(display.BUTTON_B)
    pressed['X'] = display.is_pressed(display.BUTTON_X)
    pressed['Y'] = display.is_pressed(display.BUTTON_Y)
    
    global recorded_inputs
    
    if any_button(pressed) and demo_mode == False:
        recorded_inputs.append((frameCount, pressed))
    
    return pressed


def any_button(pressed):
    return pressed['A'] or pressed['B'] or pressed['X'] or pressed['Y']


def show_title_screen(display):
    title_red, title_green, title_blue = title_color
    display.set_pen(title_red, title_green, title_blue)
    
    display.text("PiCo", int(width/6), int(height/16), 10, 8)
    display.text("Snake", int(width/16), int(height/2), 10, 8)
    
def show_level_name(display):
    title_red, title_green, title_blue = title_color
    display.set_pen(title_red, title_green, title_blue)
    
    display.text("Level", int(width/12), int(height/16), 10, 8)
    display.text(str(level_number), int(7*width/16), int(height/2), 10, 8)
    
def show_lives_left(display):
    title_red, title_green, title_blue = title_color
    display.set_pen(title_red, title_green, title_blue)
    
    display.text("Lives", int(width/12), int(height/16), 10, 8)
    display.text(str(lives_left), int(width/16), int(height/2), 10, 8)
    
def show_score(display):    
    score_red, score_green, score_blue = score_color
    display.set_pen(score_red, score_green, score_blue)
    
    display.text("SCORE", int(width/16), int(height/16), 10, 8)
    display.text(str(score), int(2*width/5), int(height/2), 10, 8)
    
def show_game_over(display):    
    score_red, score_green, score_blue = score_color
    display.set_pen(score_red, score_green, score_blue)
    
    display.text("Game", int(width/6), int(height/16), 10, 8)
    display.text("Over", int(width/16), int(height/2), 10, 8)


def draw_background(display):
    wall_red, wall_blue, wall_green = wall_color
    display.set_pen(wall_red, wall_blue, wall_green)
        
    
    display.set_pen(0, 0, 0)
    display.clear()
    #display.rectangle(2, 2, 236, 128) # arena
    
    
def draw_game_objects(display):        
    food.show(display)   
    draw_walls(display) 
    snake.show(display)

def draw_walls(display):
    wall_red, wall_blue, wall_green = wall_color
    
    for wall in walls:
        grid_x, grid_y = wall
        tile_x = grid_x * tile_size
        tile_y = grid_y * tile_size
        
        display.set_pen(wall_red, wall_blue, wall_green)
        display.rectangle(tile_x, tile_y, tile_size, tile_size)
        display.set_pen(wall_red//2, wall_blue//2, wall_green//2)
        display.rectangle(tile_x+2, tile_y+2, tile_size-4, tile_size-4)
        
#         canvas_x = (tile_size * grid_x)
#         canvas_y = (tile_size * grid_y)
#         
#         center_x = canvas_x+(tile_size//2)
#         center_y = canvas_y+(tile_size//2)
#         radius = (tile_size-4)//2
#         
#         display.circle(center_x, center_y, radius)
        
level_number = 0
total_levels = 4

    
game_state = {"title_screen": 0,
              "level_name": 1,          
              "lives_left": 2,
              "playing": 3,              
              "show_score": 4,
              "game_over": 5}

state = game_state['title_screen']

recorded_inputs = [
    (780, {'A': False, 'X': False, 'Y': True, 'B': False}),
    (860, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (882, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (891, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (927, {'A': False, 'X': False, 'Y': False, 'B': True}),
    (936, {'A': False, 'X': False, 'Y': False, 'B': True}),
    (954, {'A': False, 'X': False, 'Y': True, 'B': False}),
    (963, {'A': False, 'X': False, 'Y': True, 'B': False}),
    (999, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (1017, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (1080, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (1098, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (1188, {'A': False, 'X': False, 'Y': False, 'B': True}),
    (1260, {'A': False, 'X': False, 'Y': True, 'B': False}),
    (1323, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (1332, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (1368, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (1395, {'A': False, 'X': False, 'Y': False, 'B': True}),
    (1422, {'A': False, 'X': False, 'Y': True, 'B': False}),
    (1503, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (1512, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (1539, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (1584, {'A': False, 'X': False, 'Y': False, 'B': True}),
    (1638, {'A': False, 'X': False, 'Y': True, 'B': False}),
    (1692, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (1728, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (1764, {'A': False, 'X': False, 'Y': False, 'B': True}),
    (1800, {'A': False, 'X': False, 'Y': True, 'B': False}),
    (1809, {'A': False, 'X': False, 'Y': True, 'B': False}),
    (1836, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (1872, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (1926, {'A': False, 'X': False, 'Y': False, 'B': True}),
    (1962, {'A': False, 'X': False, 'Y': True, 'B': False}),
    (1998, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (2025, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (2034, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (2070, {'A': False, 'X': False, 'Y': False, 'B': True}),
    (2079, {'A': False, 'X': False, 'Y': False, 'B': True}),
    (2106, {'A': False, 'X': False, 'Y': True, 'B': False}),
    (2133, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (2142, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (2169, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (2178, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (2224, {'A': False, 'X': False, 'Y': False, 'B': True}),
    (2240, {'A': False, 'X': False, 'Y': True, 'B': False}),
    (2248, {'A': False, 'X': False, 'Y': True, 'B': False}),
    (2304, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (2328, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (2360, {'A': False, 'X': False, 'Y': False, 'B': True}),
    (2368, {'A': False, 'X': False, 'Y': True, 'B': False}),
    (2432, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (2456, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (2480, {'A': False, 'X': False, 'Y': False, 'B': True}),
    (2496, {'A': False, 'X': False, 'Y': True, 'B': False}),
    (2544, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (2552, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (2568, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (2592, {'A': False, 'X': False, 'Y': False, 'B': True}),
    (2608, {'A': False, 'X': False, 'Y': True, 'B': False}),
    (2632, {'A': False, 'X': True, 'Y': False, 'B': False}),
    (2640, {'A': True, 'X': False, 'Y': False, 'B': False}),
    (2648, {'A': True, 'X': False, 'Y': False, 'B': False})
    ]

def map_to_range(val, min_1, max_1, min_2, max_2):
    if val <= min_1:
        return min_2
    elif val >= max_1:
        return max_2
    else:
        diff_1 = max_1 - min_1
        ratio_1 = (val-min_1)/diff_1
        
        #min_2, max_2 = min(min_2, max_2), max(min_2, max_2)
        
        diff_2 = max_2 - min_2
        ratio_2 = (ratio_1*diff_2)
        
        
        ratio_2 += min_2
        
        return ratio_2

print(map_to_range(5, 0, 10, 50, 100))
print(map_to_range(3, 1, 10, 100, 2))
score = 0

base_refresh = 0.01

countdown = 20
cooldown = countdown


min_skip, max_skip = 10, 2

#recorded_inputs = []
    
demo_mode = True

def demo_movements(pressed):
    global recorded_inputs
    print(recorded_inputs[0][0], frameCount)
    if recorded_inputs[0][0] <= frameCount:
        print("tryin")                                                                                                                                                                                                                                                                                    
        this_move = recorded_inputs.pop(0)
        return this_move[1]
    else:
        return pressed
        

def init_level():
    global snake, food, score
    load_level(level_number)
    snake = Snake()
    food = Food()
    #frameCount = 0
    score = 0

while True:    
    
    frame_skip = int(map_to_range(score, 0, 50, min_skip, max_skip))
    
    if frameCount % frame_skip == 0:
        pressed = update_inputs(display)
        #draw_background(display)
        
        #debug_pattern()
        
        if state == game_state['title_screen']:
            cooldown -= 1
            
            
            lives_left = 3
            
            draw_background(display)
            show_title_screen(display)
            
            if cooldown < 0:
                cooldown = countdown
                state = game_state['level_name']
                init_level()
                
                
        
        elif state == game_state['level_name']:
            cooldown -= 1
            
            draw_background(display)
            show_level_name(display)
            
            if cooldown < 0:
                cooldown = countdown
                state = game_state['lives_left']
                
                
        elif state == game_state['lives_left']:
            cooldown -= 1
            
            draw_background(display)
            show_lives_left(display)
            
            if cooldown < 0:
                state = game_state['playing']
        
        
        elif state == game_state['playing']:        
                
            draw_background(display)
            draw_game_objects(display)
            
            if demo_mode:
                pressed = demo_movements(pressed)
            
            snake.update_direction(pressed)
            new_head = snake.move()

            if new_head.pos == food.pos:
                score += 1
                snake.push(new_head)
                food.reset_position()
                
            elif (snake.moving() and (snake.contains(new_head.pos) or check_walls(new_head.pos))):
                #state = game_state['game_over']
                cooldown = 10
                                    
                state = game_state['show_score']
                
                if demo_mode == False:
                    for inp in recorded_inputs:
                        print(inp, end=",\n")
                    
                    recorded_inputs = []
            
            else:
                snake.push(new_head)
                snake.pop()
                
        elif state == game_state['show_score']:
            cooldown -= 1
            
            draw_background(display)
            draw_game_objects(display)
            show_score(display)
            
            if cooldown < 0:
                cooldown = countdown
                
                if score > 3:
                    level_number += 1
                    level_number %= total_levels
                else:                    
                    lives_left -= 1
                    
                if lives_left == 0:
                    state = game_state['game_over']
                else:
                    init_level()
                    state = game_state['level_name']
                        
            
        
        elif state == game_state['game_over']:
            cooldown -= 1
            
            draw_background(display)
            draw_game_objects(display)
            show_game_over(display)
            
            if cooldown < 0:     
                cooldown = countdown           
                state = game_state['title_screen']

        display.update()
        
    frameCount += 1
    utime.sleep(base_refresh)