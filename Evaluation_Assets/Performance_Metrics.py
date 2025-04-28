"""
Performance_Metrics Class

This class calculates performance metrics for the system, including Coverage Percentage, Violations, Connectivity, and Turnaround Time.
This class also calculates the feasibility and connectivity metrics.


@ Author            Reda Ghanem
@ Version           1.0
@ Last update       11/11/2023
"""

# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ********************  importing libraries and classes  ************************ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #

# [1]- importing libraries
import numpy as np

# [2]- importing Classes and Functions
from .Undirected_Graph import Undirected_Graph               # for Undirected_Graph class
from Boids_Assets.Helper_Functions import *                  # for helper functions ex. normalize_speed_limit ...

# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #



# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
# ┃--------------------- # Performance_Metrics Class # ------------------------┃ #
# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #

class Performance_Metrics:

    def __init__(self, constants):

        self.Cons = constants  # receive Constants and Global variables from main code

        # Incremental Value to calculate the percentage of the time that the robots are moving without violating and disconnected
        self.incremental_value = round(1/self.Cons.ITERATIONS_PER_SECOND, 2)

        # Variables for Area Coverage Problem

        # Local Unexplored-Frontier-Coverage-Obstacles Matrix for short called UFCO Matrix, The matrix will filled later with values
        # 0 for Unexplored cell
        # 1 for Frontier cell
        # 2 for Explored cell
        # 3 for Obstacle cell
        # Create an array filled with zeros, since all celles Unexplored at first step
        self.GLOBAL_UFCO_MATRIX = np.zeros((self.Cons.UFCO_MATRIX_ROWS, self.Cons.UFCO_MATRIX_COLUMNS), dtype=int)
        self.FRONTIERS_LIST       = []    # collect all valid frontier cells at time 𝑡 into a list of frontier cells

        # Helper Result Variables
        self.EXPERIMENT_RUNTIME      = 0          # Real world runtime of the Experiment
        self.COVERAGE_COUNT          = 0          # count number of explored and obstacles cells at step t
        self.PREVIOUS_COVERAGE_COUNT = 0          # count number of explored and obstacles cells at step (t-1)
        self.CONNECTIVITY_GRAPH      = Undirected_Graph(self.Cons.NUM_OF_ROBOTS)  # to check the connectivity between robots

        # Main Result Variables (Performance Metrics)
        self.VIOLATIONS              = 0         # count the number of robot-robot collisions and robot-obstacle collisions and robot-out arena
        self.COVERAGE_PERCENTAGE     = 0         # the percentage of the known area that has been visited by all robots
        self.TURNAROUND_TIME         = 0         # measuring the time taken by robots to cover the environment

        

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Update All Results (Performance Metrics)
    def updat_performance_metrics(self, boids, start_time, current_time, time_step):


        self.EXPERIMENT_RUNTIME = current_time - start_time             # update EXPERIMENT_RUNTIME

        self.updata_GLOBAL_UFCO_MATRIX(boids)                           # update GLOBAL_UFCO_MATRIX and COVERAGE_COUNT

        self.update_turnaround_time(time_step)                          # update TURNAROUND_TIME (TT)
        
        self.update_violations(boids)                                   # update VIOLATIONS (V)

        self.update_COVERAGE_PERCENTAGE()                               # update COVERAGE_PERCENTAGE (CP)



    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to update supervisor GLOBAL_UFCO_MATRIX from shared boids ufco_matrices of all robots
    def updata_GLOBAL_UFCO_MATRIX(self, boids):

        # Loop over all robots to update GLOBAL_UFCO_MATRIX from shared robots ufco_matrices
        for boid in boids:
            robot_ufco_matrix = boid.ufco_matrix

            # Element-wise maximum operation
            self.GLOBAL_UFCO_MATRIX = np.maximum(robot_ufco_matrix, self.GLOBAL_UFCO_MATRIX)

            # Count the occurrences of 2 and 3 in the result_matrix
            count_explored_and_obstacle_cells = np.count_nonzero(self.GLOBAL_UFCO_MATRIX >= 2)

            self.COVERAGE_COUNT = count_explored_and_obstacle_cells

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to update TURNAROUND_TIME
    def update_turnaround_time(self, time_step):
        # update TURNAROUND_TIME (TT), each ITERATIONS_PER_SECOND step we assume it as one sec, so each ITERATIONS_PER_SECOND we got speed 25 cm(pixel) per sec
        self.TURNAROUND_TIME = time_step/self.Cons.ITERATIONS_PER_SECOND

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to update COVERAGE_PERCENTAGE
    def update_COVERAGE_PERCENTAGE(self):
        self.COVERAGE_PERCENTAGE = (self.COVERAGE_COUNT/self.Cons.TOTAL_CELLS)*100      # update COVERAGE_PERCENTAGE (CP)
        self.COVERAGE_PERCENTAGE = round(self.COVERAGE_PERCENTAGE, 2)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to increment the number of violations if any violations (robot-robot collisions), (robot-obstacle collisions), or (robot-out-of-arena) occur
    def update_violations(self, boids):

        violations_flag = False  # initial value for violations_flage

        for i, boid in enumerate(boids):

            # Case [1]: Check for collisions between current robot and all other robots: (robot-robot collisions)
            for other_boid in boids[i+1:]:
                distance = calculate_distance(boid.position, other_boid.position)
                if distance < (self.Cons.ROBOT_RADIUS*2):  # Adjust the collision distance threshold as needed
                    violations_flag = True

                # Another check for Connectivity Metric: are these two robots connected or not
                if distance < self.Cons.SHARE_RANGE:
                    # Add an edge between the two connected robots if the edge doesn't already exist
                    self.CONNECTIVITY_GRAPH.add_edge(boid.id, other_boid.id)

                else:
                    # Remove the edge between the two unconnected robots if the edge exists
                    self.CONNECTIVITY_GRAPH.remove_edge(boid.id, other_boid.id)


            # Case [2]: Check for collisions between robots and obstacles: (robot-obstacle collisions)
            for obstacle_position in self.Cons.OBSTACLES_POSITIONS:
                distance = calculate_distance(boid.position, obstacle_position)
                if distance < (self.Cons.CELL_SIZE/2 + self.Cons.ROBOT_RADIUS):  # Adjust the collision distance threshold as needed
                    violations_flag = True


            # Case [3]: Check if the (robot center) is out of the arena: (robot-out-of-arena)
            if boid.x < 0 or boid.x > self.Cons.ARENA_WIDTH:
                violations_flag = True
            if boid.y < 0 or boid.y > self.Cons.ARENA_LENGTH:
                violations_flag = True

            
            # # We can use also another way to check for violations: (robot-out-of-arena)
            # # Case [3]: Check if the (robot body) is out of the arena
            # if boid.x < (0 + ROBOT_RADIUS) or boid.x > (ARENA_WIDTH - ROBOT_RADIUS):
            #     VIOLATIONS += 1
            # if boid.y < (0 + ROBOT_RADIUS) or boid.y > (ARENA_LENGTH - ROBOT_RADIUS):
            #     VIOLATIONS += 1


        # Update VIOLATIONS (V)
        if violations_flag:
            self.VIOLATIONS = round(self.VIOLATIONS + self.incremental_value, 2)
        



   

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to check if coverage task is completed or not
    def check_task_completed(self):

        # Step for optimization
        # Check if TT > MAX_STOP_TIME or all GLOBAL_UFCO_MATRIX cells explored (2 or 3)
        if self.TURNAROUND_TIME >= self.Cons.MAX_STOP_TIME or self.COVERAGE_COUNT >= self.Cons.TOTAL_CELLS:
            
            # to avoid any additional time because parallel runs 100 iteration per second
            if self.TURNAROUND_TIME >= self.Cons.MAX_STOP_TIME:
                self.TURNAROUND_TIME = self.Cons.MAX_STOP_TIME
            
            if self.COVERAGE_COUNT >= self.Cons.TOTAL_CELLS:
                self.COVERAGE_COUNT = self.Cons.TOTAL_CELLS

            return True
        
        return False
