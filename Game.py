import pygame
from pygame import gfxdraw
import json
import math

""" Parent class for a 5x5 grid pygame """

class Game:

    def __init__(self, game):
        self.game = game
        self.row_num, self.col_num = 5, 5

        # Initialises matrix grid with 0's
        self.matrix = [[0 for _ in range(self.row_num)] for _ in range(self.col_num)]

        # Size of the game window
        self.update_screen()

        # Create the give up button
        self.give_up_button = pygame.Rect(self.width//2 - 50, self.height - 60, 100, 50)
        
        # Create a dictionary to map matrix values to colors
        self.colors = {0: (128, 128, 128),  # grey
                1: (0, 255, 0),        # green
                2: (255, 255, 0),      # yellow
                3: (255, 0, 0),        # red
                4: (64, 224, 208)}     # turquoise
        
        self.highscore = self.get_highscore()
        self.score = 0
        self.max_time = 20
        self.screen = pygame.display.set_mode(self.size)
        self.game_difficulty = math.inf

    def update_screen(self):
        """ Updates screen size """
        self.width = self.row_num * 100
        self.height = self.col_num * 100 + 60
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
        self.screen.blit(give_up_text, (self.width//2 - 50 , self.height - 45))

        for _ in range(3):
            for num in [0, 1]:
                matrix = [[num for _ in range(self.row_num)] for _ in range(self.col_num)]
                # Draw the circles
                for i in range(self.col_num):
                    for j in range(self.row_num):
                        color = self.colors[matrix[i][j]]
                        gfxdraw.aacircle(self.screen, (i*100+50), (j*100+50), 40, color)
                        gfxdraw.filled_circle(self.screen, (i*100+50), (j*100+50), 40, color)
                pygame.event.pump()
                pygame.display.flip()
                pygame.time.wait(500)

    def lose(self):
        """ Runs when game is finished, flashes all circles red 3 times, and calls update_highscore() if necessary """

        self.update_screen()

        if self.score > self.highscore:
            self.update_highscore(self.score)

        for _ in range(3):
            for num in [0,3]:
                matrix = [[num for _ in range(self.row_num)] for _ in range(self.col_num)]
                # Draw the circles
                for i in range(self.col_num):
                    for j in range(self.row_num):
                        color = self.colors[matrix[i][j]]
                        gfxdraw.aacircle(self.screen, (i*100+50), (j*100+50), 40, color)
                        gfxdraw.filled_circle(self.screen, (i*100+50), (j*100+50), 40, color)
                pygame.event.pump()
                pygame.display.flip()
                pygame.time.wait(500)

    def get_highscore(self):
        """ Returns the highscore for the current game """

        with open("high_scores.json", "r") as f:
            highscores = json.load(f)
        return highscores[self.game]

    def update_highscore(self):
        """ Updates the highscore for he current game """

        with open("high_scores.json", "r+") as f:
            highscores = json.load(f)
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
        font = pygame.font.Font(None, 30)

        # Create the give up button text
        give_up_text = font.render("Give Up", True, (255,255,255))

        # Create the give up button
        self.give_up_button = pygame.Rect(self.width//2 - 50, self.height - 60, 100, 50)

        # Draw the give up button
        self.screen.blit(give_up_text, (self.give_up_button.x + (self.give_up_button.width/2 - give_up_text.get_width()/2), self.give_up_button.y + (self.give_up_button.height/2 - give_up_text.get_height()/2)))
        pygame.draw.rect(self.screen, (255, 0, 0), self.give_up_button, 2)


        # Draw the circles
        for i in range(self.col_num):
            for j in range(self.row_num):
                color = self.colors[self.matrix[i][j]]
                gfxdraw.aacircle(self.screen, (i*100+50), (j*100+50), 40, color)
                gfxdraw.filled_circle(self.screen, (i*100+50), (j*100+50), 40, color)

        # Draw the score
        score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (self.width - 150, self.height - 25))

        # Calculate the time remaining
        time_remaining = round(self.max_time - (self.time_passed / 1000), 2)

        # Create a text surface with the time remaining
        text = font.render(str(time_remaining), True, (255, 255, 255))

        # Draw the text surface on the screen at the bottom left corner
        self.screen.blit(text, (10, self.height - 25))

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
        easy_button = pygame.Rect(self.width//2 - 100, self.height//2 - 75, 200, 50)
        easy_text = font.render("Easy", True, (255, 255, 255))

        # Create the memory button
        medium_button = pygame.Rect(self.width//2 - 100, self.height//2, 200, 50)
        medium_text = font.render("Medium", True, (255, 255, 255))

        hard_button = pygame.Rect(self.width//2 - 100, self.height//2 + 75, 200, 50)
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
                        self.row_num = 4
                        self.col_num = 4
                        running = False
                    elif medium_button.collidepoint(pos):
                        self.row_num = 5
                        self.col_num = 5
                        running = False
                    elif hard_button.collidepoint(pos):
                        self.row_num = 6
                        self.col_num = 6
                        running = False
                self.update_screen()

            # Draw the buttons on the screen
            self.screen.fill((0, 0, 0))
            self.screen.blit(easy_text, (self.width//2 - easy_text.get_width()//2, self.height//2 - 60))
            pygame.draw.rect(self.screen, (255, 255, 255), easy_button, 2)
            self.screen.blit(medium_text, (self.width//2 - medium_text.get_width()//2, self.height//2 + 15))
            pygame.draw.rect(self.screen, (255, 255, 255), medium_button, 2)
            self.screen.blit(hard_text, (self.width//2 - hard_text.get_width()//2, self.height//2 + 90))
            pygame.draw.rect(self.screen, (255, 255, 255), hard_button, 2)
            pygame.display.update()
        
        