import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the initial integer
integer = 1



# Set up the window in fullscreen mode
window = pygame.display.set_mode((1728, 1080), FULLSCREEN)

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Set up the fonts
font = pygame.font.Font(None, 52)  # For the main number
debug_font = pygame.font.Font(None, 18)  # For the debug grids

# Key mapping for readability
key_mapping = {"l": "L", "a": "A"}

def render_grid(surface, items, rows, cols, start_x, start_y, line_height):
    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            if index < len(items):
                # Use GREEN for the most recent keypress, WHITE for others
                color = GREEN if index == len(items) - 1 else WHITE
                rendered_item = str(key_mapping.get(items[index], str(items[index])))
                text = debug_font.render(rendered_item, True, color)
                text_x = start_x + col * 53  # Adjust column spacing
                text_y = start_y + row * line_height
                surface.blit(text, (text_x, text_y))
# Function to update the display
def update_display(current_integer, keystrokes, numbers, debug_mode):
    # Clear the screen
    window.fill(BLACK)

    # Render the main number
    number_text = font.render(str(current_integer), True, WHITE)
    number_rect = number_text.get_rect(center=window.get_rect().center)
    window.blit(number_text, number_rect)

    if debug_mode:
        # Render the keystrokes grid above the number
        render_grid(
            window,
            keystrokes[-256:],  # Last 256 keystrokes
            rows=8,
            cols=32,
            start_x=35,
            start_y=number_rect.top - 500,
            line_height=40,
        )

        # Render the numbers grid below the number
        render_grid(
            window,
            numbers[-256:],  # Last 256 numbers
            rows=8,
            cols=32,
            start_x=35,
            start_y=number_rect.bottom + 200,
            line_height=40,
        )

    # Update the display
    pygame.display.flip()

# Initialize variables for tracking
keystrokes = ["a"]  # To store the most recent 256 keystrokes
numbers = [integer]  # To store the most recent 256 integers
debug_mode = False  # Debug mode is initially off

# Function to handle key presses and track history
def handle_key_press(key):
    global integer, keystrokes, numbers

    # Add the key to the keystrokes list
    keystrokes.append(key)
    if len(keystrokes) > 256:  # Keep only the most recent 256 keystrokes
        keystrokes.pop(0)

    # Modify the integer based on key press
    if key == "l":
        if numbers[-1] == 1:
            integer += 1
        else:
            if keystrokes[-4:] == ["l", "l", "l", "l"]:
                integer //= 2
            elif keystrokes[-4:] == ["a", "a", "a", "l"]:
                if all(num*2 > numbers[-1] for num in numbers[-8:-1]):
                    integer *= 8
                else:
                    integer //= 100
            else:
                integer += 4
    
    elif key == "a":
        if keystrokes[-12:] == ["a","a","a","a","a","a","a","a","a","a","a","a"]:
            if all(num*2 > numbers[-1] for num in numbers[-8:-1]):
                if numbers[0] != 1:
                    integer **= 1024
                else:
                    integer *= 1024
            else:
                integer //= 100
        else:
            integer //= 1.25
            integer = int(integer)
    if "lalallll" in "".join(keystrokes[-16:]):
        integer += 32
    # Check for repeated sequences
    for length in range(2, 9):
        if len(keystrokes) >= length * 3:
            sequence = keystrokes[-length:]
            if sequence[0] != "a" and keystrokes[-length*2:-length] == sequence and keystrokes[-length*3:-length*2] == sequence:
                integer = 1
                break
        


    # Add the new integer to the numbers list
    numbers.append(integer)
    if len(numbers) > 256:  # Keep only the most recent 256 integers
        numbers.pop(0)

    return integer

# Initial display update
update_display(integer, keystrokes, numbers, debug_mode)

# Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_BACKQUOTE:  # Toggle debug mode with the backtick key
                debug_mode = not debug_mode
                update_display(integer, keystrokes, numbers, debug_mode)
            elif event.key == K_l:  # Press "L"
                current_integer = handle_key_press("l")
                update_display(current_integer, keystrokes, numbers, debug_mode)
            elif event.key == K_a:  # Press "A"
                current_integer = handle_key_press("a")
                update_display(current_integer, keystrokes, numbers, debug_mode)