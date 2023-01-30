import pygame
import json
import random

from Game import Game


""" Class containing the snake pygame """

class SnakeGame(Game):

    def __init__(self):
        super().__init__("Snake")
        self.snake = [(0, self.row_num//2), (1, self.row_num//2)]
        self.running = True
        self.current_dir = (1, 0)

        super().difficulty_screen()

    def set_next_food(self):
        """ Sets the next location of the snake food """
        run = True
        while run:
            self.next_food = (random.randint(0, self.row_num-1), random.randint(0, self.col_num-1))
            if self.next_food not in self.snake:
                run = False

        self.matrix[self.next_food[0]][self.next_food[1]] = 2
        self.render_game()

    def move_snake(self):
        """ Moves snake in the given direction 
        Inputs:
        -------
        direction - (x, y) for -1 <= x, y <= 1 """

        tail_x, tail_y = self.snake[0][0], self.snake[0][1]
        head_x, head_y = self.snake[-1][0], self.snake[-1][1]


        # Position of new head of the snake, loops around if out of bounds
        new_head = ((head_x + self.current_dir[0]), (head_y + self.current_dir[1]))
        if new_head[0] > (self.row_num-1):
            new_head = (0, new_head[1])
        if new_head[0] < 0:
            new_head = ((self.row_num-1), new_head[1])
        if new_head[1] > (self.col_num-1):
            new_head = (new_head[0], 0)
        if new_head[1] < 0:
            new_head = (new_head[0], (self.col_num-1))

        # If snake hits itself
        if new_head in self.snake:
            self.matrix[head_x][head_y] = 4
            self.lose(new_head)
            return
        
        # If the snake picks up food
        if new_head == self.next_food:
            self.increase_snake()

        # Update matrix to show snake
        self.matrix[tail_x][tail_y] = 6
        self.matrix[head_x][head_y] = 4
        self.matrix[new_head[0]][new_head[1]] = 5
        
        # Update snake list
        del self.snake[0]
        self.snake.append(new_head)


    def increase_snake(self):
        """ Adds another circle to the tail of the snake """

        # Calculate where to put the new tail based off of the current tail orientation
        tail = (self.snake[0][0], self.snake[0][1])
        dir = ((self.current_dir[0]*-1), (self.current_dir[1]*-1))
        new_tail = ((tail[0] + dir[0]), (tail[1] + dir[1]))

        # Add new tail to the snake
        self.snake = [new_tail] + self.snake
        self.set_next_food()
    
    def lose(self, new_head):
        if self.score > self.highscore:
            self.update_highscore()

        for _ in range(3):
            for colour in [3, 5]:
                self.matrix[new_head[0]][new_head[1]] = colour
                self.render_game()
                pygame.time.wait(400)
        self.running = False

    def change_direction(self, new_dir):
        """ Changes the snakes direction if its not opposite the current direction """

        result = ((self.current_dir[0] + new_dir[0]), (self.current_dir[1], + new_dir[1]))
        if not result == (0, 0):
            self.current_dir = new_dir

    def run(self):
        """ Runs the main game loop """
        self.start()
        self.matrix = [[6 for _ in range(self.row_num)] for _ in range(self.col_num)]
        self.set_next_food()

        # Set the title of the window
        pygame.display.set_caption("Memory Game")
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_mode(self.size)

        # Create clock object
        clock = pygame.time.Clock()

        move_wait = 400

        while self.running:
            # Resets the clicked circle back to a grey after the flash_time interval
            if self.time_passed > move_wait:
                self.time_passed = 0
                self.move_snake()

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.change_direction((-1,0))
                    elif event.key == pygame.K_RIGHT:
                        self.change_direction((1,0))
                    elif event.key == pygame.K_UP:
                        self.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.change_direction((0, 1))
                
            self.render_game()
            self.time_passed += clock.tick(30)
