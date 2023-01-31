import pygame
import json
import random

from Game import Game


""" Class containing the matching pygame """

class MatchingGame(Game):

    def __init__(self):
        super().__init__("Matching")
        self.flipped_circle = None
        super().difficulty_screen()
        
    def generate_answer_matrix(self):
        """ Generates the locations of the colours"""
        self.answer_matrix = [[0 for _ in range(self.col_num)] for _ in range(self.row_num)]
        grid_size = self.row_num * self.col_num
        colour_list = []
        # loop through the colours
        for key, val in self.colors.items():
            # end the loop if there is enough colours already
            if len(colour_list) == grid_size:
                break
            # add the colour if it is not black or grey
            if val != (128, 128, 128) and val != (0, 0, 0):
                colour_list.append(key)
                colour_list.append(key)

        # shuffle the colour list
        random.shuffle(colour_list)

        counter = 0
        for i in range(self.row_num):
            for j in range(self.col_num):
                self.answer_matrix[i][j] = colour_list[counter]
                counter += 1

    def flip_circle(self, circle):
        """ Flips over the selected circle """
        
        i, j = circle
        # If the user clicks on a matched circle
        if self.matrix[i][j] == 6 or circle == self.flipped_circle:
            return
        self.matrix[i][j] = self.answer_matrix[i][j]
        self.render_game()

        # If the user is matching a circle
        if self.flipped_circle:
            fl_i, fl_j = self.flipped_circle
            self.flipped_circle = None
            self.score += 1
            # If the circles are the same colour
            if self.answer_matrix[i][j] == self.answer_matrix[fl_i][fl_j]:
                self.matrix[fl_i][fl_j] = 6
                self.matrix[i][j] = 6
                # If all the circles are cleared
                if all(row == [6 for _ in range (self.col_num)] for row in self.matrix):
                    self.update_highscore(reverse=True)
                    self.start()
                    self.running = False
            else:
                pygame.time.wait(300)
                self.matrix[fl_i][fl_j] = 0
                self.matrix[i][j] = 0
            return
    
        self.flipped_circle = circle

    def run(self):
        """ Runs the main game loop """
        
        self.generate_answer_matrix()
        # Set the title of the window
        pygame.display.set_caption("Matching Game")
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_mode(self.size)
        # Create clock object
        clock = pygame.time.Clock()

        # Create a loop to run the game
        self.running = True
        self.start()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the position of the mouse click
                    pos = pygame.mouse.get_pos()

                    # Check if the user clicks on a circle
                    for i in range(self.row_num):
                        for j in range(self.col_num):
                            circle = pygame.Rect(j*100, i*100, 80, 80)
                            if circle.collidepoint(pos):
                                self.flip_circle((i, j))

                    # Check if the user clicks on the give up button
                    if self.give_up_button.collidepoint(pos):
                        super().lose()
                        self.running = False

            self.render_game()