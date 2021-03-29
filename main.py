# import modules for timing, display, enums, and random integers
import utime
from random import randint
import picodisplay as display

# initialize some global variables for settings
backlight_intensity = 0.8

tile_size = 12
grid_w, grid_h = 20, 11 # 20*11 tiles

score = 0

snake_color = (0, 200, 0)
food_color  = (200, 0, 0)
wall_color  = (255, 0, 255)
title_color = (255, 255, 0)
score_color = (255, 255, 255)

# picodisplay boilerplate code
width = display.get_width()
height = display.get_height()

display_buffer = bytearray(width * height * 2)
display.init(display_buffer)

display.set_backlight(backlight_intensity)


'''Classes: Food, SnakeNode, Snake'''
class Food:
    def __init__(self, snake):
        self.reset_position(snake)
        
        
    def reset_position(self, s):
        self.pos = randint(1, grid_w-2), randint(1, grid_h-2)
        
        global snake
        
        while snake.contains(self.pos):
            self.pos = randint(1, grid_w-2), randint(1, grid_h-2)
            print("moving food again")


    def show(self, display):
        food_x, food_y = self.pos
    
        food_red, food_green, food_blue = food_color
        display.set_pen(food_red, food_green, food_blue)
    
        tile_x = (tile_size * food_x) + tile_size//2
        tile_y = (tile_size * food_y) + tile_size//2
        
        radius = (tile_size-2)//2
                
        display.circle(tile_x, tile_y, radius)



class SnakeNode:
    def __init__(self, position=None, direction=None, next=None):
        self.pos = position
        self.dir = direction
        self.next = next



class Snake:
    def __init__(self):
        center_of_grid = grid_w//2, grid_h//2
        self.head = SnakeNode(center_of_grid, None, None)
        self.direction = (0, 0)
        
        
    def push(self, new_head):
        new_head.next = self.head
        self.head = new_head
        
        
    def pop(self):
        current_node = self.head        
        previous_node = None
        
        while current_node.next != None:
            previous_node = current_node
            current_node = current_node.next
        
        if previous_node != None:
            previous_node.next = None
        
    
    def contains(self, position):
        current_node = self.head
        
        while current_node != None:
            if current_node.pos == position:
                return True
            
            current_node = current_node.next
            
        return False
    
        
    def move(self):
        x_dir, y_dir = self.direction        
        head_x, head_y = self.head.pos
        
        head_x += x_dir
        head_y += y_dir
        
        head_x %= grid_w
        head_y %= grid_h
        
        new_head_position = head_x, head_y        
        new_node = SnakeNode(new_head_position, self.direction, None)
        
        return new_node


    def show(self, display):
        snake_red, snake_green, snake_blue = snake_color
        display.set_pen(snake_red, snake_green, snake_blue)
        
        current_node = self.head
        
        while current_node != None:            
            if current_node != self.head:
                display.set_pen(0, 255, 0)
                
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
                grid_x, grid_y = current_node.pos
            
                canvas_x = (tile_size * grid_x)
                canvas_y = (tile_size * grid_y)
                
                center_x = canvas_x+(tile_size//2)
                center_y = canvas_y+(tile_size//2)
                radius = (tile_size-4)//2
                
                display.set_pen(0, 255, 0)
                display.circle(center_x, center_y, radius)
            
            previous_node = current_node
            current_node = current_node.next
        
        
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
    
    return pressed


def any_button(pressed):
    return pressed['A'] or pressed['B'] or pressed['X'] or pressed['Y']


def show_title_screen(display):
    title_red, title_green, title_blue = title_color
    display.set_pen(title_red, title_green, title_blue)
    
    display.text("PiCo", int(width/6), int(height/16), 10, 8)
    display.text("Snake", int(width/16), int(height/2), 10, 8)
    
    
def show_game_over(display):    
    score_red, score_green, score_blue = score_color
    display.set_pen(score_red, score_green, score_blue)
    
    display.text("SCORE", int(width/16), int(height/16), 10, 8)
    display.text(str(score), int(2*width/5), int(height/2), 10, 8)


def draw_background(display):
    wall_red, wall_blue, wall_green = wall_color
    display.set_pen(wall_red, wall_blue, wall_green)
    display.clear()    
    
    display.set_pen(0, 0, 0)
    display.rectangle(2, 2, 236, 128) # arena
    
    
def draw_game_objects(display):
    food.show(display)    
    snake.show(display)        

    
game_state = {"title_screen": 0,
              "playing": 1,
              "game_over": 2}

state = game_state['title_screen']


snake = Snake()
food = Food(snake)

score = 0

while True:    
    pressed = update_inputs(display)
    
    draw_background(display)
    
    #debug_pattern()
    
    if state == game_state['title_screen']:
        show_title_screen(display)
        
        if any_button(pressed):
            state = game_state['playing']
    
    
    elif state == game_state['playing']:
        draw_game_objects(display)
        
        snake.update_direction(pressed)
        new_head = snake.move()

        #if snake.check_food(new_head, food): 
            #snake.push(new_head)
        if new_head.pos == food.pos:
            score += 1
            
            food.reset_position(0)
            
            while snake.contains(food.pos):
                food.reset_position(0)
                print("moving food again!!!")
            
            snake.push(new_head)
            
#         elif snake.check_walls(new_head) or (snake.moving() and snake.contains(new_head.pos)):
        elif (snake.moving() and snake.contains(new_head.pos)):
            state = game_state['game_over']
            
        else:
            snake.push(new_head)
            snake.pop()
    
    
    elif state == game_state['game_over']:
        draw_game_objects(display)
        show_game_over(display)
        
        if any_button(pressed):
            score = 0
            snake = Snake()
            food = Food(snake)
            state = game_state['title_screen']

    display.update()
    utime.sleep(0.1)