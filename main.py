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


# initialize global variables for game (used by all classes)
tile_size = 12 # size in pixels of square tiles
grid_w, grid_h = 20, 11 # 20*11 tiles


# initialize global color data
snake_color = (0, 200, 0)
food_color  = (200, 0, 0)
wall_color  = (200, 0, 200)
title_color = (255, 255, 0)
score_color = (255, 255, 255)

    
class Level:
    def __init__(self, level_number):
        self.load_level(level_number)
        
        
    def load_level(self, level_number):
        self.walls = []
        
        filename = "level-" + str(level_number) + ".txt"
        f = open(filename, "r")
        lines = f.readlines()

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if 0 <= x < grid_w and 0 <= y < grid_h and char == '0':
                    wall_pos = x, y
                    self.walls.append(wall_pos)
                    
        f.close()
        
        
    def check_walls(self, pos):
        for wall in self.walls:
            if pos == wall:
                return True
        
        return False
        
        
    def show(self, display):
        wall_red, wall_blue, wall_green = wall_color
        
        for wall in self.walls:
            grid_x, grid_y = wall
            tile_x = grid_x * tile_size
            tile_y = grid_y * tile_size
            
            display.set_pen(wall_red, wall_blue, wall_green)
            display.rectangle(tile_x, tile_y, tile_size, tile_size)
            display.set_pen(wall_red//2, wall_blue//2, wall_green//2)
            display.rectangle(tile_x+2, tile_y+2, tile_size-4, tile_size-4)
            


class Food:
    def __init__(self, snake, level):
        self.reset_position(snake, level)
        
        
    # sets new position for Food (bug: allows new position in snake...?)
    def reset_position(self, snake, level):
        new_pos = randint(1, grid_w-2), randint(1, grid_h-2)
        
        while snake.contains(new_pos) or level.check_walls(new_pos):
            new_pos = randint(1, grid_w-2), randint(1, grid_h-2)
            
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
                return True
            
            current_node = current_node.next
            
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
                    self.line(x1, y1, x2, y2)
                
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
        
        
    def moving(self):
        return self.direction != (0, 0)


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


    def line(self, x1, y1, x2, y2):
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
        
        
        
class SnakeNode:
    def __init__(self, position=None, direction=None, next=None, prev=None):
        self.pos = position
        self.dir = direction
        self.next = next

        

class Game:        
    def __init__(self):
        self.pressed = {}
        self.frameCount = 0
        self.score = 0

        self.base_refresh = 0.01

        self.countdown = 20
        self.cooldown = self.countdown

        self.min_skip, self.max_skip = 10, 2

        self.level_number = 0
        self.total_levels = 4

        self.game_state = {"title_screen": 0,
                          "level_name": 1,          
                          "lives_left": 2,
                          "playing": 3,              
                          "show_score": 4,
                          "game_over": 5}

        self.state = self.game_state['title_screen']
        
        
    # initialize current level
    def init_level(self):
        self.level = Level(self.level_number)
        self.snake = Snake()
        self.food = Food(self.snake, self.level)
        self.score = 0    
        
        
    # update game data
    def tick(self, display):
        self.frame_skip = int(self.map_to_range(self.score, 0, 50, self.min_skip, self.max_skip))
    
        if self.frameCount % self.frame_skip == 0:
            self.update_inputs(display)
            self.draw_background(display)
            
            if self.state == self.game_state['playing']:        
                    
                self.draw_game_objects(display)            
                
                self.snake.update_direction(self.pressed)
                new_head = self.snake.move()

                if new_head.pos == self.food.pos:
                    self.score += 1
                    self.snake.push(new_head)
                    self.food.reset_position(self.snake, self.level)
                    
                elif (self.snake.moving() and (self.snake.contains(new_head.pos) or self.level.check_walls(new_head.pos))):
                    self.cooldown = self.countdown                                 
                    self.state = self.game_state['show_score']
                
                else:
                    self.snake.push(new_head)
                    self.snake.pop()
                    
            else:
                self.cooldown -= 1    
                self.show_game_text(display)
                
                if self.cooldown < 0:
                    self.cooldown = self.countdown
                    
                    if self.state == self.game_state['title_screen']: 
                        self.lives_left = 3
                        self.level_number = 0
                        self.state = self.game_state['level_name']                 
                    
                    elif self.state == self.game_state['level_name']: 
                        self.init_level()  
                        self.state = self.game_state['lives_left']                        
                            
                    elif self.state == self.game_state['lives_left']:   
                        self.state = self.game_state['playing']            
                            
                    elif self.state == self.game_state['show_score']:                             
                        if self.score > 3:
                            self.level_number += 1
                            self.level_number %= self.total_levels
                        else:                    
                            self.lives_left -= 1
                            
                        if self.lives_left == 0:
                            self.state = self.game_state['game_over']
                        else:                        
                            self.state = self.game_state['level_name'] 
                    
                    elif self.state == self.game_state['game_over']:           
                         self.state = self.game_state['title_screen']

            display.update()
            
        self.frameCount += 1
        utime.sleep(self.base_refresh)
        
        
    # user input button methods
    def update_inputs(self, display):        
        self.pressed['A'] = display.is_pressed(display.BUTTON_A)
        self.pressed['B'] = display.is_pressed(display.BUTTON_B)
        self.pressed['X'] = display.is_pressed(display.BUTTON_X)
        self.pressed['Y'] = display.is_pressed(display.BUTTON_Y)        


    def any_button(self, pressed):
        return self.pressed['A'] or self.pressed['B'] or self.pressed['X'] or self.pressed['Y']


    # graphics methods
    def draw_background(self, display):
        display.set_pen(0, 0, 0)
        display.clear()
        
        
    def draw_game_objects(self, display):        
        self.food.show(display)   
        self.level.show(display) 
        self.snake.show(display)
        
        
    def show_game_text(self, display):
        title_red, title_green, title_blue = title_color
        display.set_pen(title_red, title_green, title_blue)

        if self.state == self.game_state['title_screen']:
            display.text("PiCo", int(width/6), int(height/16), 10, 8)
            display.text("Snake", int(width/16), int(height/2), 10, 8)
            
        elif self.state == self.game_state['level_name']:    
            display.text("Level", int(width/12), int(height/16), 10, 8)
            display.text(str(self.level_number), int(7*width/16), int(height/2), 10, 8)
            
        elif self.state == self.game_state['lives_left']:    
            display.text("Lives", int(width/12), int(height/16), 10, 8)
            display.text(str(self.lives_left), int(width/16), int(height/2), 10, 8)
            
        elif self.state == self.game_state['show_score']:
            self.draw_game_objects(display)
            display.set_pen(title_red, title_green, title_blue)
            display.text("SCORE", int(width/16), int(height/16), 10, 8)
            display.text(str(self.score), int(2*width/5), int(height/2), 10, 8)
        
        elif self.state == self.game_state['game_over']:
            self.draw_game_objects(display)
            display.set_pen(title_red, title_green, title_blue)
            display.text("Game", int(width/6), int(height/16), 10, 8)
            display.text("Over", int(width/16), int(height/2), 10, 8)


    def debug_pattern(self, display):
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


    # simple range mapping method
    def map_to_range(self, val, min_1, max_1, min_2, max_2):
        if val <= min_1:
            return min_2
        elif val >= max_1:
            return max_2
        else:
            diff_1 = max_1 - min_1
            ratio_1 = (val-min_1)/diff_1
            
            diff_2 = max_2 - min_2
            ratio_2 = (ratio_1*diff_2) + min_2
            
            return ratio_2
        


# initialize game
game = Game()

# run game loop
while True:    
    game.tick(display)