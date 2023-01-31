import pygame
from pygame import gfxdraw
import json
from enum import Enum
import os

""" Parent class for a 5x5 grid pygame """

class Game:

    def __init__(self, game):
        self.game = game
        self.row_num, self.col_num = 5, 5

        # Initialises matrix grid with 0's
        self.matrix = [[0 for _ in range(self.col_num)] for _ in range(self.row_num)]

        # Size of the game window
        self.update_screen()

        # Create the give up button
        self.give_up_button = pygame.Rect(self.width//2 - 50, self.height - 60, 100, 50)
        
        # Create a dictionary to map matrix values to colors
        self.colors = {
                0: (128, 128, 128),    # grey
                1: (0, 255, 0),        # green
                2: (255, 255, 0),      # yellow
                3: (255, 0, 0),        # red
                4: (64, 224, 208),     # turquoise
                5: (32, 112, 208),     # blue
                6: (0, 0, 0),          # black
                7: (138,43,226),       # purple
                8: (245, 66, 152),     # pink
                9: (156, 25, 49),      # maroon
                10: (24, 71, 27),      # dark green
                11: (89, 47, 28),      # brown
                12: (144, 245, 151),   # pale green
                13: (162, 173, 36),    # mustard
                14: (0, 0, 0),         # white
                15: (214, 113, 4),     # orange
                16: (32, 19, 209),     # dark blue
                17: (184, 93, 81),     # pale red
                }     
        
        self.game_difficulty = difficulty.NONE
        self.get_highscore()
        self.score = 0
        self.max_time = 20
        self.time_passed = 0
        self.screen = pygame.display.set_mode(self.size)

    def update_screen(self):
        """ Updates screen size """

        self.width = self.col_num * 100
        self.height = self.row_num * 100 + 60
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)

        # Clear the screen
        self.screen.fill((0, 0, 0))
        

    def start(self):
        """ Flashes all circles Green 3 times """
        self.update_screen()

        # Create the font
        font = pygame.font.Font(None, 30)

        # Create the give up button text
        give_up_text = font.render("Highscore: " + str(self.highscore), True, (255,255,255))
        self.screen.blit(give_up_text, (self.width//2 - ((11 + len(str(self.highscore))) * 5) , self.height - 45))

        for _ in range(1):
            for num in [0, 1]:
                matrix = [[num for _ in range(self.col_num)] for _ in range(self.row_num)]
                # Draw the circles 
                for i in range(self.row_num):
                    for j in range(self.col_num):
                        color = self.colors[matrix[i][j]]
                        gfxdraw.aacircle(self.screen, (j*100+50), (i*100+50), 40, color)
                        gfxdraw.filled_circle(self.screen, (j*100+50), (i*100+50), 40, color)
                pygame.event.pump()
                pygame.display.flip()
                pygame.time.wait(250)
        self.update_screen()

    def lose(self):
        """ Runs when game is finished, flashes all circles red 3 times, and calls update_highscore() if necessary """

        self.update_screen()

        self.update_highscore()

        font = pygame.font.Font(None, 25)
        # Draw the score
        score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (self.width - ((7.55 + min(4, len(str(self.highscore)))) * 11), self.give_up_button.y - 15 + (self.give_up_button.height/2 - self.give_up_text.get_height()/2)))
        # Draw the highscore
        highscore_text = font.render("Highscore: " + str(self.highscore), True, (255, 255, 255))
        self.screen.blit(highscore_text, (self.width - ((11 + min(4, len(str(self.highscore)))) * 11), 15 + self.give_up_button.y + (self.give_up_button.height/2 - self.give_up_text.get_height()/2)))


        for _ in range(3):
            for num in [0,3]:
                matrix = [[num for _ in range(self.col_num)] for _ in range(self.row_num)]
                # Draw the circles
                for i in range(self.row_num):
                    for j in range(self.col_num):
                        color = self.colors[matrix[i][j]]
                        gfxdraw.aacircle(self.screen, (j*100+50), (i*100+50), 40, color)
                        gfxdraw.filled_circle(self.screen, (j*100+50), (i*100+50), 40, color)                
                pygame.event.pump()
                pygame.display.flip()
                pygame.time.wait(500)
        self.update_screen()

    def get_highscore(self):
        """ Returns the highscore for the current game """

        if not os.path.exists('matrices.json'):
            setup_matrices()
        if not os.path.exists('high_scores.json'):
            setup_highscores()

        with open("high_scores.json", "r") as f:
            highscores = json.load(f)
        
        if self.game_difficulty != difficulty.NONE:
            self.highscore = highscores[self.game][self.game_difficulty.name]
        else:
            self.highscore = highscores[self.game]

    def update_highscore(self, reverse=False):
        """ Updates the highscore for he current game """

        if ((reverse == False) and (self.score > self.highscore)) or ((reverse == True) and (self.score < self.highscore)):
            with open("high_scores.json", "r+") as f:
                highscores = json.load(f)
                if self.game_difficulty != difficulty.NONE:
                    highscores[self.game][self.game_difficulty.name] = self.score
                else:
                    highscores[self.game] = self.score
                f.seek(0)
                json.dump(highscores, f)
                f.truncate()

            self.highscore = self.score

    def run(self):
        """ Main game loop for the game """
        pass
    
    def render_game(self):
        """ Renders the game screen """
        # Clear the screen
        self.screen.fill((0, 0, 0))

        # Create the font
        font = pygame.font.Font(None, 25)

        # Create the give up button text
        self.give_up_text = font.render("Give Up", True, (255,255,255))

        # Create the give up button
        self.give_up_button = pygame.Rect(self.width//2 - 50, self.height - 50, 100, 40)

        # Draw the give up button
        self.screen.blit(self.give_up_text, (self.give_up_button.x + (self.give_up_button.width/2 - self.give_up_text.get_width()/2), self.give_up_button.y + (self.give_up_button.height/2 - self.give_up_text.get_height()/2)))
        pygame.draw.rect(self.screen, (255, 0, 0), self.give_up_button, 2)

        # Draw the circles
        for i in range(self.row_num):
            for j in range(self.col_num):
                color = self.colors[self.matrix[i][j]]
                gfxdraw.aacircle(self.screen, (j*100+50), (i*100+50), 40, color)
                gfxdraw.filled_circle(self.screen, (j*100+50), (i*100+50), 40, color)

        # Draw the score
        score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (self.width - ((7.55 + min(4, len(str(self.highscore)))) * 11), self.give_up_button.y - 15 + (self.give_up_button.height/2 - self.give_up_text.get_height()/2)))
        # Draw the highscore
        highscore_text = font.render("Best score: " + str(self.highscore), True, (255, 255, 255))
        self.screen.blit(highscore_text, (self.width - ((12 + min(4, len(str(self.highscore)))) * 11), 15 + self.give_up_button.y + (self.give_up_button.height/2 - self.give_up_text.get_height()/2)))

        # Calculate the time remaining
        time_remaining = round(self.max_time - (self.time_passed / 1000), 2)

        # Create a text surface with the time remaining
        time_text = font.render(str(time_remaining), True, (255, 255, 255))

        # Draw the text surface on the screen at the bottom left corner
        self.screen.blit(time_text, (10, self.give_up_button.y + (self.give_up_button.height/2 - self.give_up_text.get_height()/2)))

        # Update the display
        pygame.display.flip()
    
    def difficulty_screen(self):
        """ Displays the difficulty screen """

        self.screen = pygame.display.set_mode(self.size)
        # Set the title of the window
        pygame.display.set_caption("Game Menu")

        # Create the font
        font = pygame.font.Font(None, 30)

        # Create the run_trace button
        easy_button = pygame.Rect(self.width//2 - 100, self.height//3 - 75, 200, 50)
        easy_text = font.render("Easy", True, (255, 255, 255))

        # Create the memory button
        medium_button = pygame.Rect(self.width//2 - 100, self.height//3, 200, 50)
        medium_text = font.render("Medium", True, (255, 255, 255))

        hard_button = pygame.Rect(self.width//2 - 100, self.height//3 + 75, 200, 50)
        hard_text = font.render("Hard", True, (255, 255, 255))

        # Create a loop to run the menu
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if easy_button.collidepoint(pos):
                        self.set_diffculty(difficulty.EASY)
                        running = False

                    elif medium_button.collidepoint(pos):
                        self.set_diffculty(difficulty.MEDIUM)
                        running = False

                    elif hard_button.collidepoint(pos):
                        self.set_diffculty(difficulty.HARD)
                        running = False

            # Draw the buttons on the screen
            self.screen.fill((0, 0, 0))
            self.screen.blit(easy_text, (self.width//2 - easy_text.get_width()//2, self.height//3 - 60))
            pygame.draw.rect(self.screen, (255, 255, 255), easy_button, 2)
            self.screen.blit(medium_text, (self.width//2 - medium_text.get_width()//2, self.height//3 + 15))
            pygame.draw.rect(self.screen, (255, 255, 255), medium_button, 2)
            self.screen.blit(hard_text, (self.width//2 - hard_text.get_width()//2, self.height//3 + 90))
            pygame.draw.rect(self.screen, (255, 255, 255), hard_button, 2)
            pygame.display.update()
    
    def set_diffculty(self, complexity):
        """ Sets the difficulty paramaters for the different games """

        self.game_difficulty = complexity
        if self.game == "Memory" or self.game == "Snake":
            if self.game_difficulty == difficulty.EASY:
                self.row_num = 4
                self.col_num = 4
            elif self.game_difficulty == difficulty.MEDIUM:
                self.row_num = 5
                self.col_num = 5
            elif self.game_difficulty == difficulty.HARD:
                self.row_num = 6
                self.col_num = 6
        elif self.game == "Matching":
            if self.game_difficulty == difficulty.EASY:
                self.row_num = 2
                self.col_num = 5
            elif self.game_difficulty == difficulty.MEDIUM:
                self.row_num = 4
                self.col_num = 5
            elif self.game_difficulty == difficulty.HARD:
                self.row_num = 6
                self.col_num = 5
        self.matrix = [[0 for _ in range(self.col_num)] for _ in range(self.row_num)]
        
        self.get_highscore()
        self.run()


class difficulty(Enum):
    NONE = 0,
    EASY = 1,
    MEDIUM = 2,
    HARD = 3

def setup_highscores():
    with open('high_scores.json', 'w') as f: 
        json.dump({"Memory": {"EASY": 0, "MEDIUM": 0, "HARD": 0}, "Trace": 0, "Snake": {"EASY": 0, "MEDIUM": 0, "HARD": 0}}, f)

def setup_matrices():
    with open('matrices.json', 'w') as f:
        json.dump({"1": [[[0, 1, 0, 0, 0], [1, 0, 1, 0, 0], [0, 1, 0, 1, 0], [0, 0, 1, 0, 1], [0, 0, 0, 1, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 2, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]], [[1, 0, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 2, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 1, 1, 1, 2], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]], 
                    "2": [[[0, 0, 0, 0, 0], [0, 2, 3, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 2, 0, 0], [1, 2, 0, 0, 0], [0, 0, 1, 0, 0]], [[0, 0, 0, 2, 0], [0, 0, 3, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 2, 0, 0], [0, 1, 0, 0, 0], [1, 0, 0, 0, 0]]], 
                    "3": [[[0, 0, 1, 1, 0], [0, 1, 3, 2, 0], [0, 0, 1, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 1, 2, 1, 0], [0, 2, 0, 0, 0], [0, 1, 2, 3, 0], [0, 0, 0, 1, 0]]], 
                    "4": [[[0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [0, 1, 3, 0, 1], [0, 0, 0, 1, 0], [0, 0, 0, 0, 0]], [[1, 2, 1, 0, 2], [0, 0, 0, 3, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 1, 0], [1, 0, 2, 0, 0], [0, 3, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 2, 0, 0], [0, 0, 0, 3, 0], [0, 0, 1, 0, 1]]], 
                    "5": [[[0, 0, 0, 0, 1], [0, 0, 0, 0, 2], [0, 1, 0, 0, 2], [2, 0, 0, 0, 2], [3, 2, 1, 2, 3]], [[0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [0, 1, 0, 0, 2], [2, 0, 0, 1, 0], [2, 2, 3, 1, 0]], [[0, 0, 0, 0, 0], [0, 2, 0, 0, 0], [0, 0, 3, 0, 0], [0, 0, 0, 3, 0], [0, 0, 0, 0, 2]]], 
                    "6": [[[0, 0, 0, 0, 0], [0, 1, 0, 1, 0], [0, 2, 3, 2, 0], [0, 0, 1, 3, 2], [2, 2, 1, 1, 0]], [[0, 2, 1, 0, 0], [0, 1, 0, 3, 0], [0, 0, 0, 2, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]], 
                    "7": [[[1, 2, 0, 0, 0], [1, 3, 1, 0, 0], [0, 2, 0, 0, 0], [0, 3, 2, 1, 0], [0, 0, 0, 3, 2]], [[0, 0, 0, 0, 0], [0, 3, 3, 0, 0], [3, 0, 0, 1, 0], [0, 2, 1, 0, 0], [0, 0, 0, 0, 0]]], 
                    "8": [[[1, 0, 0, 0, 2], [2, 3, 1, 0, 3], [0, 2, 2, 2, 0], [0, 0, 3, 0, 0], [0, 2, 2, 3, 1]], [[0, 0, 0, 0, 1], [0, 2, 0, 2, 0], [0, 0, 3, 0, 2], [0, 1, 0, 1, 0], [0, 0, 0, 0, 0]]], 
                    "9": [[[2, 0, 0, 3, 3], [3, 0, 2, 0, 2], [0, 2, 0, 1, 2], [0, 2, 3, 2, 1], [1, 0, 1, 2, 0]], [[2, 1, 3, 2, 1], [1, 0, 0, 2, 0], [0, 0, 3, 0, 0], [0, 2, 0, 2, 0], [1, 0, 0, 0, 1]]], 
                    "10": [[[0, 0, 2, 0, 0], [0, 1, 1, 3, 2], [0, 2, 3, 2, 1], [3, 2, 0, 2, 2], [2, 0, 2, 3, 2]], [[2, 0, 0, 1, 3], [1, 3, 0, 0, 2], [2, 0, 1, 0, 1], [2, 0, 0, 2, 2], [0, 1, 0, 0, 3]], [[2, 0, 0, 0, 0], [0, 3, 1, 0, 0], [0, 2, 3, 0, 2], [1, 0, 0, 3, 0], [2, 3, 2, 0, 0]], [[0, 0, 0, 0, 0], [0, 2, 0, 0, 0], [0, 0, 3, 0, 0], [1, 0, 0, 2, 0], [0, 3, 2, 0, 1]]]
                    }, f)
