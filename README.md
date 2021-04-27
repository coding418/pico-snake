# Pico Snake
Written in MicroPython for Raspberry Pi Pico and Pimoroni Pico Display

## Animated GIF Preview (12 fps)
![Pico Snake](./img/pico-snake.gif)

[Download Long MP4 Preview](https://github.com/coding418/pico-snake/blob/main/vid/pico-snake.mp4?raw=true)



## Requirements
### Hardware:

[Raspberry Pi Pico](https://www.raspberrypi.org/products/raspberry-pi-pico/)

[Pimoroni Pico Display](https://shop.pimoroni.com/products/pico-display-pack)

### Software:

[Custom MicroPython Image by Pimoroni](https://github.com/pimoroni/pimoroni-pico/releases)

## Design

### Classes
* Game
	* Manages the main game data (e.g. score), states (e.g. title screen, playing, game over) and functionality (e.g. intialize level, update game, get input, draw game objects)

* Snake
	* A singly-linked list to represent the Snake. Contains:
		* data about the Snake (e.g. pointer to "head" SnakeNode, current direction)
		* methods (e.g. push new head node, pop tail node, check if a given co-ordinate is occupied by a SnakeNode, update direction, draw)

* SnakeNode
	* Single node in the Snake linked list. Each node has: a position, a direction, and a pointer to the next node in the list.

* Food
	* Represents food for the Snake. Each instance has a position and methods to draw the food and reset the position to a random location. 
	* The reset_position() method ensures that the new position is not inside the Snake or inside any walls in the level.

* Level
	* Loads level data from a txt file, stores the position of the walls inside each level, draws the walls, and checks if a position is inside the walls.
	* Each level is a 20x11 grid.
	* Each cell in the grid can contain either a SnakeNode, a piece of Food, a wall, or nothing.
	* Levels are designed through a txt file:
		* Each line of the file represents a row in the grid.
		* Each character in a line represents a cell in the grid.
		* The first 20 characters of each of the first 11 lines represent the level grid (any characters or lines outside of that are ignored).
		* A '0' character represents a wall, a ' ' character (i.e. a space) represents an empty cell in the grid. 
			* Technically, any character other than '0' represents an empty cell since all other characters are currently ignored by the Level class.
			* It would be relatively simple to add other types of walls or level objects using this system: they would simply be represented by another character.