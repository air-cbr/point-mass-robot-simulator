
"""
Robot class

This class represents a robot in the simulation.

@ Author            Reda Ghanem
@ Version           1.0
@ Last update       11/11/2023
"""

# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ********************  importing libraries and classes  ************************ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #

# [1]- importing Classes and Functions
from Boids_Assets.Boid import Boid

# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #


# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
# ┃--------------------------- # Robot Class # --------------------------------┃ #
# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #

class Robot:
    def __init__(self, constants, start_position, start_heading_angle, robot_size, robot_img, robot_id):

        self.Cons = constants  # receive Constants and Global variables from main code

        # Create Boid object
        self.boid = Boid(self.Cons, start_position, start_heading_angle, robot_size, robot_id)
        self.robot_img_path = robot_img         # The original image path


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to update the robot's position and heading angle
    def update_ufco_matrix_coverage(self):
        # Check if boid get into a new cell and update ufco_matrix for coverage
        self.boid.update_ufco_matrix_coverage()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to Collect neighbor IDs, positions, velocities, and ufco_matrix data by Receiving data from other robots
    def receive_information(self, robtos):

        # clear all old neighbors data
        self.boid.clear_neighbors_data()

        for neighbor_robot in robtos:
            if neighbor_robot != self:
                self.boid.neighbors_IDs.append(neighbor_robot.boid.id)
                self.boid.neighbors_positions.append(neighbor_robot.boid.position)
                self.boid.neighbors_velocities.append(neighbor_robot.boid.velocity)
                self.boid.neighbors_ufco_matrices.append(neighbor_robot.boid.ufco_matrix)



