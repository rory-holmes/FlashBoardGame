import random
import pygame
from pygame import gfxdraw

from Game import Game

""" Class containing the memory pygame """

class MemoryGame(Game):

    def __init__(self):
        super().__init__("Memory")
        self.score = 0
        self.time_passed = 0
        self.max_time = 10
        # Create a variable to store the current pattern
        self.pattern = [(random.randint(0, self.row_num-1), random.randint(0, self.col_num-1))]

        super().difficulty_screen()

    def show_pattern(self):
        """ Runs the animation to show the current pattern """

        self.matrix = [[0 for _ in range(self.row_num)] for _ in range(self.col_num)]
        self.render_game()
        pygame.time.wait(500)

        for x, y in self.pattern:
            self.matrix[x][y] = 4
            # Draw the circles
            for i in range(self.row_num):
                for j in range(self.col_num):
                    color = self.colors[self.matrix[i][j]]
                    gfxdraw.aacircle(self.screen, (i*100+50), (j*100+50), 40, color)
                    gfxdraw.filled_circle(self.screen, (i*100+50), (j*100+50), 40, color)

            pygame.event.pump()
            pygame.display.flip()
            pygame.time.wait(700)
            self.matrix[x][y] = 0
    
        self.matrix = [[0 for _ in range(self.row_num)] for _ in range(self.col_num)]
        self.render_game()
        pygame.time.wait(300)
        self.time_passed = 0


    def add_to_pattern(self):
        """ Adds a random circle to the current pattern """

        while True:
            next_circle = (random.randint(0, self.row_num-1), random.randint(0, self.col_num-1))
            if next_circle not in self.pattern:
                self.pattern.append(next_circle)
                return

    def lose(self, current_index, cl_i, cl_j):
        """ Overides game loss to instead display the incorrect click """
        
        i, j = self.pattern[current_index][0], self.pattern[current_index][1]

        if self.score > self.highscore:
            self.update_highscore()

        for _ in range(3):
            for colour in [(3,4), (0, 0)]:
                self.matrix[cl_i][cl_j] = colour[0]
                self.matrix[i][j] = colour[1]
                self.render_game()
                if colour != (0, 0):
                    pygame.time.wait(400)
                
                pygame.time.wait(250)

    def run(self):
        """ Runs the main game loop """

        # Set the title of the window
        pygame.display.set_caption("Memory Game")
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_mode(self.size)
        # Create clock object
        clock = pygame.time.Clock()

        # Create a variable to store the current circle
        current_index = 0

        # Create a loop to run the game
        running = True
        self.start()
        self.show_pattern()
        flash_time = 120
        time_passed_lc = 0
        next_level = False

        while running:
            # Resets the clicked circle back to a grey after the flash_time interval
            if time_passed_lc > flash_time:
                i, j = self.pattern[current_index-1]
                self.matrix[i][j] = 0
            # If max time has passed
            if self.time_passed > self.max_time * 1000:
                # Restart Game
                super().lose()
                running = False
            # Runs the next level animation
            if next_level:
                next_level = False
                self.show_pattern()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the position of the mouse click
                    pos = pygame.mouse.get_pos()

                    # Check if the user clicks on a circle
                    for i in range(self.col_num):
                        for j in range(self.row_num):
                            circle = pygame.Rect(i*100, j*100, 80, 80)
                            if circle.collidepoint(pos):
                                # Check if the corect circle is clicked
                                if (i, j) == self.pattern[current_index]:
                                    current_index += 1
                                    self.matrix[i][j] = 2
                                    time_passed_lc = 0
                                    self.score += 1
                                    # Check if all the circles in the pattern have been clicked
                                    if current_index >= len(self.pattern):
                                        self.matrix[i][j] = 1
                                        current_index = 0
                                        self.add_to_pattern()
                                        next_level = True
                                else:
                                    # Incorrect circle clicked, lose game
                                    self.lose(current_index, i, j)
                                    running = False

                    # Check if the user clicks on the give up button
                    if self.give_up_button.collidepoint(pos):
                        super().lose()
                        running = False

            self.render_game()

            # Get the time that has passed since the last frame
            self.time_passed += clock.tick(30)
            time_passed_lc += clock.tick(30)
