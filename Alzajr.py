import pygame
import sys
from pygame.locals import FULLSCREEN, QUIT, KEYDOWN, K_BACKQUOTE, K_l, K_a, K_ESCAPE

class AlzajrGame:
    def __init__(self):
        pygame.init()
        self.screen_info = pygame.display.Info()
        self.screen_width, self.screen_height = self.screen_info.current_w, self.screen_info.current_h
        self.is_fullscreen = False
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Alzajr")
        self.start_logo = pygame.image.load("Alzajr.png").convert_alpha()
        self.logo_width, self.logo_height = 512, 512
        self.scaled_logo = pygame.transform.scale(self.start_logo, (min(self.logo_width, self.logo_height), min(self.logo_width, self.logo_height)))
        self.start_logo = pygame.transform.scale(self.start_logo, (512, 512))
        self.base_font_size = 52
        self.font = pygame.font.Font(None, self.base_font_size)
        self.debug_font = pygame.font.Font(None, 18)
        self.cursive_font = pygame.font.Font(pygame.font.match_font('cursive'), 36)
        self.key_mapping = {"l": "L", "a": "A"}
        self.integer = 1
        self.keystrokes = ["a"]
        self.numbers = [self.integer]
        self.debug_mode = False
        self.paused = True
        self.resizing = False
        self.BLACK = (0, 0, 0) 
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.center_logo()
        self.update_display()

    def center_logo(self):
        self.window.fill((0, 0, 0))
        logo_x = (self.window.get_width() - self.scaled_logo.get_width()) // 2
        logo_y = (self.window.get_height() - self.scaled_logo.get_height()) // 2
        self.window.blit(self.scaled_logo, (logo_x, logo_y))
        pygame.display.flip()

    def resize_elements(self, window_width, window_height):
        logo_size = min(window_width, window_height) // 3
        self.scaled_logo = pygame.transform.scale(self.start_logo, (logo_size, logo_size))
        self.font = pygame.font.SysFont("Baskerville", max(20, self.base_font_size * window_width // self.screen_width), bold=True)
        self.debug_font = pygame.font.SysFont("Baskerville", max(10, 18 * window_width // self.screen_width))
        self.cursive_font = pygame.font.SysFont("Baskerville", max(18, 24 * window_width // self.screen_width), bold=True, italic=True)
        self.center_logo()

    def render_grid(self, surface, items, rows, cols, start_x, start_y, cell_width, cell_height):
        for row in range(rows):
            for col in range(cols):
                index = row * cols + col
                if index < len(items):
                    color = self.GREEN if index == len(items) - 1 else self.WHITE
                    rendered_item = str(self.key_mapping.get(items[index], str(items[index])))
                    text = self.debug_font.render(rendered_item, True, color)
                    text_x = start_x + col * cell_width
                    text_y = start_y + row * cell_height
                    surface.blit(text, (text_x, text_y))

    def update_display(self):
        self.window.fill(self.BLACK)
        if self.paused:
            self.center_logo()
            text = "Press A and L to begin"
            text_surface = self.cursive_font.render(text, True, self.WHITE)
            text_rect = text_surface.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2 + 100))
            self.window.blit(text_surface, text_rect)
        else:
            number_text = self.font.render(str(self.integer), True, self.WHITE)
            number_rect = number_text.get_rect(center=self.window.get_rect().center)
            self.window.blit(number_text, number_rect)
            if self.debug_mode:
                grid_cell_width = self.window.get_width() // 32
                grid_cell_height = self.window.get_height() // 32
                self.render_grid(self.window, self.keystrokes[-256:], 8, 32, 10, 10, grid_cell_width, grid_cell_height)
                self.render_grid(self.window, self.numbers[-256:], 8, 32, 10, self.window.get_height()-(0.25*self.window.get_height()), grid_cell_width, grid_cell_height)
        pygame.display.flip()

    def handle_key_press(self, key):
        self.keystrokes.append(key)
        if len(self.keystrokes) > 256:
            self.keystrokes.pop(0)
        self.integer = int(self.integer)
        if self.integer >= 2**32:
            self.integer = 2**32 - 1
        if self.integer >= 999999999:
            self.integer %= 999999999
        elif key == "l":
            if self.numbers[-1] == 1:
                self.integer += 1
            else:
                if "lllllalllll" in "".join(self.keystrokes[-32:]):
                    self.integer = int(str(self.integer) + "0")
                elif self.keystrokes[-4:] == ["l", "l", "l", "l"]:
                    self.integer //= 2
                elif self.keystrokes[-4:] == ["a", "a", "a", "l"]:
                    if all(num*2 > self.numbers[-1] for num in self.numbers[-8:-1]):
                        self.integer *= 8
                    else:
                        self.integer //= 100
                else:
                    self.integer += 4
        elif key == "a":
            if "lllllalllll" in "".join(self.keystrokes[-32:]):
                self.integer -= 1
            elif self.keystrokes[-12:] == ["a","a","a","a","a","a","a","a","a","a","a","a"]:
                if all(num*2 > self.numbers[-1] for num in self.numbers[-8:-1]):
                    if self.numbers[0] == 412:
                        self.integer **= 1024
                    else:
                        self.integer *= 1024
                else:
                    self.integer //= 100
            else:
                self.integer //= 1.25
                self.integer = int(self.integer)
        if "lalallll" in "".join(self.keystrokes[-16:]):
            self.integer += 32
        for length in range(2, 9):
            if len(self.keystrokes) >= length * 5:
                sequence = self.keystrokes[-length:]
                if sequence[0] != "a" and self.keystrokes[-length*5:-length*4] == sequence and self.keystrokes[-length*4:-length*3] == sequence and self.keystrokes[-length*2:-length] == sequence and self.keystrokes[-length*3:-length*2] == sequence:
                    self.integer = 1
                    break
        self.numbers.append(self.integer)
        if len(self.numbers) > 256:
            self.numbers.pop(0)
        return self.integer

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_BACKQUOTE:
                        self.debug_mode = not self.debug_mode
                        self.update_display()
                    elif event.key == K_ESCAPE:
                        self.paused = not self.paused
                        self.update_display()
                    elif not self.paused:
                        if event.key == K_l:
                            self.integer = self.handle_key_press("l")
                            self.update_display()
                        elif event.key == K_a:
                            self.integer = self.handle_key_press("a")
                            self.update_display()
                    elif self.paused and ((event.key == K_l and pygame.key.get_pressed()[K_a]) or (event.key == K_a and pygame.key.get_pressed()[K_l])):
                        self.paused = False
                        self.update_display()
                elif event.type == pygame.VIDEORESIZE:
                    self.resizing = True
                    self.window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.resize_elements(event.w, event.h)
            if self.resizing:
                self.update_display()
                self.resizing = False

if __name__ == "__main__":
    game = AlzajrGame()
    game.run()
