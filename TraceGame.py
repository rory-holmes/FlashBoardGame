import pygame
import json
import random

from Game import Game


""" Class containing the trace pygame """

class TraceGame(Game):
    
    def __init__(self):
        super().__init__("Trace")
        self.difficulty = 0
        self.current_circle = None
        self.max_time = 30
        self.run()


    def create_matrix(self):
        """ Gets a saved matrix from the matrices.json file """

        difficulty = str(self.difficulty)
        with open("matrices.json", "r") as f:
            matrices = json.load(f)
        
        # If there are multiple matrices at the same difficulty
        length = len(matrices[difficulty])
        if isinstance(matrices[difficulty][0][0], list):
            self.matrix = matrices[difficulty][random.randint(0, length-1)]
        else:
            self.matrix = matrices[difficulty]

        # Correct for a bigger matrix (all saved matrices are 5x5)

        # Correct row num
        if (self.row_num - len(self.matrix[0])) > 0:
            for row in self.matrix:
                for _ in range(self.row_num - len(self.matrix[-1])):
                    row.append(0)
        # Correct col num
        for _ in range(self.col_num- len(self.matrix)):
            self.matrix.append([0 for _ in range(self.row_num)])

    def restart_matrix(self, start=False):
        """ Resets the game variables """

        # If the game is restarting completely
        if start == True:
            self.difficulty = 1
            self.score = 0
        else:     
            self.score += 100
        self.create_matrix()
        self.current_circle = None
        self.time_passed = 0

    def start(self):
        """ Runs start animation and sets the matrix """

        super().start()
        self.restart_matrix(True)

    def clicked_circle(self, i, j):
        """ Runs when a circle is clicked """

        # Decrement the matrix value by 1
        self.matrix[i][j] -= 1
        self.current_circle = (i, j)
        self.score += 10
        # Check if all the matrix values are 0
        if all(all(val == 0 for val in row) for row in self.matrix):
            self.time_passed = 0
            if self.difficulty < 10:
                self.difficulty += 1 
            else:
                self.max_time -= 1
            self.score += 100
            self.restart_matrix()

    def run(self):
        """ Runs the main game loop """

        # Initialize the pygame library
        pygame.init()

        # Set the title of the window
        pygame.display.set_caption("Trace Game")
        pygame.display.set_mode(self.size)

        # Create a matrix of size 25 with values from 0 to 3
        self.restart_matrix(True)

        # Create clock object
        clock = pygame.time.Clock()

        # Create a loop to run the game
        running = True
        self.start()

        while running:
            # Get the time that has passed since the last frame
            self.time_passed += clock.tick(30)

            # Check if max time has passed
            if self.time_passed > self.max_time * 1000:
                # Restart Game
                self.lose()
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # When the user clicks
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the position of the mouse click
                    pos = pygame.mouse.get_pos()

                    # Check if the user clicks on a circle
                    for i in range(5):
                        for j in range(5):
                            circle = pygame.Rect(i*100, j*100, 80, 80)
                            if circle.collidepoint(pos):
                                # Check if the matrix value is not 0
                                if self.matrix[i][j] > 0:
                                    # Check if the user has already clicked on a circle
                                    if self.current_circle is not None:
                                        # Check if the clicked circle is adjacent to the current circle
                                        if abs(self.current_circle[0] - i) <= 1 and abs(self.current_circle[1] - j) <= 1 and not(self.current_circle == (i,j)):
                                            self.clicked_circle(i, j)

                                    else:
                                        self.clicked_circle(i, j)

                    # Check if the user clicks on the give up button
                    if self.give_up_button.collidepoint(pos):
                        self.lose()
                        running = False


            self.render_game()
