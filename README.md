# Pico Snake
Written in MicroPython for Raspberry Pi Pico and Pimoroni Pico Display

## Animated GIF Preview (12 fps)
![Pico Snake](./img/pico-snake.gif)

*  [Download Long MP4 Preview](https://github.com/coding418/pico-snake/blob/main/vid/pico-snake.mp4?raw=true)



## Requirements
### Hardware:

*  [Raspberry Pi Pico](https://www.raspberrypi.org/products/raspberry-pi-pico/)

*  [Pimoroni Pico Display](https://shop.pimoroni.com/products/pico-display-pack)

### Software:

*  [Custom MicroPython Image by Pimoroni (includes picodisplay library)](https://github.com/pimoroni/pimoroni-pico/releases)

## Classes
### Game
* Manages the main game data and functionality.
	* Attributes include: 
		* score
		* game states (e.g. title screen, playing, game over)  
	* Methods include:
		* initialize level data
		* update game
		* get user input
		* draw game objects

### Snake
* A singly-linked list to represent the Snake.
	* Attributes include:
		* pointer to "head" SnakeNode
		* current direction
	* Methods include:
		* push new head node
		* pop tail node
		* check if co-ordinate occupied by a SnakeNode
		* update direction
		* draw Snake

### SnakeNode
* Single node in the Snake linked list. 
	* Attributes:
		* position
		* direction
		* pointer to next node in list

### Food
* Represents food for the Snake. 
	* Attribute: 
		* position
	* Methods:
		* draw food
		* reset position to random location (always ensures new position is not inside Snake or walls)

### Level
* Represents the game arena.
	* Attribute:
		* array of wall positions
	* Methods:
		* load wall positions from txt file
		* draw walls
		* check for collisions with walls


### Level Design
* Each level is a 20x11 grid of cells.
* Each cell in the grid can contain either a SnakeNode, a piece of Food, a wall, or nothing.
* Levels are designed through a txt file:
	* Each line of the file represents a row in the grid.
	* Each character in a line represents a cell in the grid.
* The first 20 characters of each of the first 11 lines represent the level grid
	* any characters or lines outside of that are ignored
* A '0' character (i.e. zero) represents a wall, a ' ' character (i.e. space) represents an empty cell in the grid. 
	* Technically, any character other than '0' represents an empty cell since all other characters are currently ignored by the Level class.
	* It would be relatively simple to add other types of walls or level objects using this system: they would simply be represented by another character.
* Extra parameters for each level could be easily added to the lines after line 11.
	* For example, a target score for that level (currently this is hardcoded as 5 for every level to simplify testing and debugging)

For example, the file level-2.txt contains the following text:
<pre>
00000          00000
0                  0
0                  0
0                  0
                    
                    
                    
0                  0
0                  0
0                  0
00000          00000
</pre>

Which creates the following level:

![Level 2 - Pico Snake](./img/level-2.png)