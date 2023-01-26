import math
import random


class Level:
    def __init__(self, size):
        """
        Initialises Level class

        :param size: Size of the matrix
        """
        self.difficulty = 300
        self.size = size
        # Initialises game matrix
        self.matrix = [[0 for _ in range(size)] for _ in range(size)]
        self.added_points = {}
        self.max_node_value = 3

    def generate_level(self):
        """
        Generates a new level

        :return:
        """
        # Generates a random node to start on
        start_num = random.randint(0, (self.size * self.size) - 1)
        row = start_num // self.size
        col = start_num - (row * 5)

        # Adds starting node location to dictionary
        self.added_points[row, col] = 0
        current_point = (row, col)

        # Sets starting the node to 1
        self.matrix[row][col] = 1

        remaining_points = random.randint(4, min(15, self.difficulty // 5))
        while remaining_points > 0:
            direction = self.random_direction(current_point)
            if direction != (math.inf, math.inf):
                intensity = self.random_node_value(remaining_points, direction)
                self.added_points[direction] = self.sum_nearby_nodes(direction)
                self.matrix[direction[0]][direction[1]] = intensity
                remaining_points -= intensity

            current_point = random.choices(list(self.added_points.keys()))[0]
        return self.matrix



    def increment_difficulty(self):
        """
        Increments the difficulty index
        :return:
        """
        self.difficulty += 10

    def random_node_value(self, rp, cp):
        """
        Returns a random available node value

        :param rp: Remaining points left to use
        :param cp: Current point (row, col)
        :return: New value of the current point
        """
        node_sum = self.sum_nearby_nodes(cp) + 1
        if node_sum > self.max_node_value:
            node_sum = self.max_node_value

        values = []
        for i in [i for i in range(1, self.max_node_value + 1)]:
            if rp >= i and node_sum >= i:
                values.append(i)

        weights = [(self.difficulty + i) ** 5 for i in values[::-1]]

        # Normalise weights
        total = sum(weights)
        for index, i in enumerate(weights):
            weights[index] = round(i / total, 1) * 100

        return random.choices(values, weights=weights)[0] if values else 0

    def random_direction(self, cp):
        """ Selects a random node (row, col) surrounding the current point
                
        :param cp: Current point (row, col)
        :return: (row, col) of a random node next to the current point
        """
        directions = []
        for row in [-1, 0, 1]:
            row = row + cp[0]
            for col in [-1, 0, 1]:
                col = col + cp[1]
                # If it is not the current point, is not already given a value, and is a possible square
                if (row, col) != cp and (row, col) not in self.added_points:
                    if -1 < row < 5 and (row - cp[0]) < 2:
                        if -1 < col < 5 and (col - cp[1]) < 2:
                            directions.append((row, col))

        return random.choices(directions)[0] if directions else (math.inf, math.inf)

    def sum_nearby_nodes(self, cp):
        """ Calculates the sum of all nodes around the current point

        :param cp: Current point (row, col)
        :return: Maximum value of next node
        """
        node_sum = 0
        for row in [-1, 0, 1]:
            row = row + cp[0]
            for col in [-1, 0, 1]:
                col = col + cp[1]
                try:
                    node_sum += self.matrix[row][col]
                except IndexError:
                    pass

        return node_sum
    
    
Level(5).generate_level()
