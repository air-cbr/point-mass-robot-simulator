"""
Boid Class

The Boid class is a fundamental component for simulating the behavior of individual agents in a swarm.
The Boid class represents an individual agent in a swarm robotics scenario.
Boids follow specific rules, such as alignment, cohesion, separation, obstacle_avoidance_force, and frontier_force to calculate their linear and angular velocities.
This class also handles the computation of forces and velocities for each boid, including interactions with neighbors and wall avoidance.
Additionally, it manages the boid's position, heading angle, and other essential properties.

@ Author            Reda Ghanem
@ Version           1.0
@ Last update       11/11/2023
"""

# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ********************  importing libraries and classes  ************************ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #

# [1]- importing libraries
import numpy as np                  # for array operations

# [2]- importing Classes and Functions
from .Boids_Rules import Boids_Rules                        # for swarm rules ex. alignment_rule, cohesion_rule ...
from .Helper_Functions import *                   # for helper functions ex. normalize_speed_limit ...

# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #

# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
# ┃---------------------------- # Boid Class # --------------------------------┃ #
# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #

class Boid:


    def __init__(self, constants=None, start_position=[0,0], start_heading_angle=0, boid_size=[10,10], boid_id=0):

        self.Cons = constants                                   # receive Constants and Global variables from main code
        self.Boids_Rules = Boids_Rules()                        # Create an object from Boids_Rules class to access all swarm rules


        self.x, self.y              = start_position            # start_position contains [x, y] of the boid
        self.position               = [self.x, self.y]          # boid position as list [x, y]
        self.heading_angle          = start_heading_angle       # start Orientation angle of the boid



        # Calculate the forward velocity in the boids's current direction using the heading angle and the desired linear velocity
        self.delta_x                = self.Cons.MAX_LINEAR_SPEED * math.cos(self.heading_angle)
        self.delta_y                = self.Cons.MAX_LINEAR_SPEED * math.sin(self.heading_angle)
        self.delta_x, self.delta_y  = normalize_speed_limit([self.delta_x, self.delta_y], self.Cons.MIN_LINEAR_SPEED, self.Cons.MAX_LINEAR_SPEED)
        self.velocity               = [self.delta_x, self.delta_y]  # boid velocity as list [delt_x, delt_y]

        self.acceleration = 1  # acceleration
        self.delta_t = 1  # A smaller value makes updating position(x,y) and heading_angle smoother


        self.width                  = boid_size[0]                  # width of boid
        self.length                 = boid_size[1]                  # height of boid
        self.radius                 = 0.5 * math.sqrt(self.width **2 + self.length **2)

        self.id                     = boid_id                       # boid id


        # Variables for Area Coverage Problem
        # Local Unexplored-Frontier-Coverage-Obstacles Matrix for short called UFCO Matrix, The matrix will filled later with values
        # 0 for Unexplored cell
        # 1 for Frontier cell
        # 2 for Explored cell
        # 3 for Obstacle cell
        self.ufco_matrix_rows     = int(self.Cons.ARENA_LENGTH/self.Cons.CELL_SIZE)           # note when we increse ARENA_LENGTH rows incresed
        self.ufco_matrix_columns  = int(self.Cons.ARENA_WIDTH/self.Cons.CELL_SIZE)            # note when we increse ARENA_WIDTH column incresed
        # Create an array filled with zeros, since all celles Unexplored at first step
        self.ufco_matrix          = np.zeros((self.Cons.UFCO_MATRIX_ROWS, self.Cons.UFCO_MATRIX_COLUMNS), dtype=int)
        self.total_cells          = self.Cons.UFCO_MATRIX_ROWS * self.Cons.UFCO_MATRIX_COLUMNS     # Total number of cells
        self.frontiers_list       = []         # collect all valid frontier cells at time 𝑡 into a list of frontier cells
        self.coverage_count       = 0          # count number of explored and obstacles cells

        # variables to collect data from neighbors 
        self.neighbors_IDs = []
        self.neighbors_positions = []
        self.neighbors_velocities = []
        self.neighbors_ufco_matrices = []


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to update ufco_matrix with values 1 or 2 representing frontier, and explored cells respectively
    def update_ufco_matrix_coverage(self):
        # Determine the current cell indices (row, col) in which the boid is located using boid position
        cell_row = math.floor(self.y / self.Cons.CELL_SIZE)  # Row = math.floor(y / square size)
        cell_col = math.floor(self.x / self.Cons.CELL_SIZE)  # Column = math.floor(x / square size)

        # Check if the boid is still in the boundary of the environment
        if (0 <= cell_row < self.ufco_matrix_rows) and (0 <= cell_col < self.ufco_matrix_columns):

            # If the current cell is unexplored or frontier, Then mark it as (explored)
            if self.ufco_matrix[cell_row][cell_col] == 0 or self.ufco_matrix[cell_row][cell_col] == 1:
                self.ufco_matrix[cell_row][cell_col] = 2

                # Update the four surrounding cells of the current cell with value 1 to represent frontiers
                self.Boids_Rules.update_surrounding_cells_as_frontiers(self, cell_row, cell_col)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to update boid ufco_matrix from shared neighbors_ufco_matrices of neighbors which in range of SHARE_RANGE
    def share_ufco_matrix(self, neighbors_positions, neighbors_ufco_matrices):
        # Loop over all neighbors to update ufco_matrix from shared neighbors_ufco_matrices
        for neighbor_pos, neighbor_ufco_matrix in zip(neighbors_positions, neighbors_ufco_matrices):  # Use zip() to iterate over lists
            distance_diff = [self.x - neighbor_pos[0], self.y - neighbor_pos[1]]
            distance = math.sqrt(distance_diff[0] ** 2 + distance_diff[1] ** 2)
            if distance < self.Cons.SHARE_RANGE:
                
                # Update ufco_matrix with the maximum values from self.ufco_matrix and neighbor_ufco_matrix
                self.ufco_matrix = np.maximum(self.ufco_matrix, neighbor_ufco_matrix)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to update boid coverage_count and frontiers_list
    def update_coverage_count_and_frontier_list(self):


        # Find indices of cells with value 1 which represnt frontiers
        indices_of_frontiers = np.argwhere(self.ufco_matrix == 1)

        # update self.frontiers_list by convert indices to a list of [i, j] pairs then update frontiers_list 
        self.frontiers_list = indices_of_frontiers.tolist()
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to compute next step math
    def update_velocity(self):

        # Calculate boid forces
        alignment_force = self.Boids_Rules.alignment_rule(self, self.neighbors_positions, self.neighbors_velocities)
        cohesion_force = self.Boids_Rules.cohesion_rule(self, self.neighbors_positions)
        separation_force = self.Boids_Rules.separation_rule(self, self.neighbors_positions)

        obstacle_avoidance_force = self.Boids_Rules.obstacle_avoidance_rule(self)
        wall_avoidance_force = self.Boids_Rules.wall_avoidance_rule(self)

        self.update_coverage_count_and_frontier_list()

    
        if (separation_force != [0,0] or obstacle_avoidance_force != [0,0]):
            frontier_force = [0,0]
        else:
            frontier_force = self.Boids_Rules.frontier_rule(self)

    


        force_x = (
                    self.Cons.ALIGNMENT_WEIGHT            * alignment_force[0]            +
                    self.Cons.COHESION_WEIGHT             * cohesion_force[0]             +
                    self.Cons.SEPARATION_WEIGHT           * separation_force[0]           +
                    self.Cons.OBSTACLE_AVOIDANCE_WEIGHT   * obstacle_avoidance_force[0]   +
                    self.Cons.WALL_AVOIDANCE_WEIGHT       * wall_avoidance_force[0]       +
                    self.Cons.FRONTIER_WEIGHT             * frontier_force[0]
                )

        force_y = (
                    self.Cons.ALIGNMENT_WEIGHT            * alignment_force[1]            +
                    self.Cons.COHESION_WEIGHT             * cohesion_force[1]             +
                    self.Cons.SEPARATION_WEIGHT           * separation_force[1]           +
                    self.Cons.OBSTACLE_AVOIDANCE_WEIGHT   * obstacle_avoidance_force[1]   +
                    self.Cons.WALL_AVOIDANCE_WEIGHT       * wall_avoidance_force[1]       +
                    self.Cons.FRONTIER_WEIGHT             * frontier_force[1]
                )

        force_x, force_y = normalize_speed_limit([force_x, force_y], self.Cons.MIN_LINEAR_SPEED, self.Cons.MAX_LINEAR_SPEED)

        #  Update boid's velocity  # such as: 𝑣_𝑓𝑙𝑜𝑐𝑘(𝑡+1) = 𝑣_𝑓𝑙𝑜𝑐𝑘(𝑡) + 𝑏𝑜𝑖𝑑_𝑓𝑜𝑟𝑐𝑒𝑠
        self.delta_x += force_x
        self.delta_y += force_y

        # Normalize boid's velocity to limit it in range [MIN_LINEAR_SPEED, MAX_LINEAR_SPEED]
        self.delta_x, self.delta_y = normalize_speed_limit([self.delta_x, self.delta_y], self.Cons.MIN_LINEAR_SPEED, self.Cons.MAX_LINEAR_SPEED)

        # update boid velocity
        self.velocity   = [self.delta_x, self.delta_y]  # boid velocity as list [delt_x, delt_y]



    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # update boid position
    def update_position(self):

        # update boid position by adding current velocity value
        self.x += self.delta_x
        self.y += self.delta_y

        # round values to make numbers same in all OS (Windows, Linux)
        self.x, self.y = [round(v, 5) for v in [self.x, self.y]]

        # update boid position
        self.position = [self.x, self.y]  # boid position as list [x, y]

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # update boid heading_angle
    def update_heading_angle(self):
        # we ignore the heading_angle update in the point mass model
        pass

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to clear all old neighbors data
    def clear_neighbors_data(self):

        self.neighbors_IDs.clear()
        self.neighbors_positions.clear()
        self.neighbors_velocities.clear()
        self.neighbors_ufco_matrices.clear()
        
