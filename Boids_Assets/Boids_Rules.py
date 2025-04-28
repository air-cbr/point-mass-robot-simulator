"""
Boids_Rules Class

These Class are essential components of the swarm simulation, implementing key behaviors that drive the
movement of individual agents (boids) within the swarm. The functions follow the rules of alignment, cohesion,
separation, and wall avoidance to determine the agents' velocities and positions in the swarm.

@ Author            Reda Ghanem
@ Version           1.0
@ Last update       11/11/2023
"""


# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ********************  importing libraries and classes  ************************ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #

# [1]- importing libraries
import math

# [2]- importing Classes and Functions
from .Helper_Functions import *

# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #



# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
# ┃------------------------- # Boids_Rules Class # ----------------------------┃ #
# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
class Boids_Rules:


    def __init__(self):
        pass


    # ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
    # ┃----------------------- # behaviours Functions # ---------------------------┃ #
    # ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #

    # alignment rule: boids attempt to match the velocities of their neighbors
    def alignment_rule(self, boid, neighbors_positions, neighbors_velocities):

        alignment_vector = [0, 0]
        neighbor_alig_count = 0

        # calculate the sum of all neighbors velocities
        for neighbor_pos, neighbor_vel in zip(neighbors_positions, neighbors_velocities):  # Use zip() to iterate over lists
            distance = calculate_distance(boid.position, neighbor_pos)
            if distance < boid.Cons.ALIGNMENT_RANGE:
                alignment_vector[0] += neighbor_vel[0]
                alignment_vector[1] += neighbor_vel[1]
                neighbor_alig_count += 1

        if neighbor_alig_count > 0:
            # calculate the average of previous sum
            alignment_vector[0] /= neighbor_alig_count
            alignment_vector[1] /= neighbor_alig_count

            # steering match velocity = desired_velocity - current_velocity
            alignment_vector = [alignment_vector[0] - boid.delta_x, alignment_vector[1] - boid.delta_y]
            alignment_vector = normalize_speed_limit(alignment_vector, boid.Cons.MIN_LINEAR_SPEED, boid.Cons.MAX_LINEAR_SPEED)

        return alignment_vector
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # cohesion rule: boids move toward the center of mass of their neighbors
    def cohesion_rule(self, boid, neighbors_positions):
        cohesion_vector = [0, 0]
        neighbor_coh_count = 0

        # calculate the sum of all neighbors positions
        for neighbor_pos in neighbors_positions:
            distance = calculate_distance(boid.position, neighbor_pos)
            if distance < boid.Cons.COHESION_RANGE:
                cohesion_vector[0] += neighbor_pos[0]
                cohesion_vector[1] += neighbor_pos[1]
                neighbor_coh_count += 1

        if neighbor_coh_count > 0:
            # calculate the average of previous sum
            cohesion_vector[0] /= neighbor_coh_count
            cohesion_vector[1] /= neighbor_coh_count

            # steering toward position = desired_position - current_position
            cohesion_vector = [cohesion_vector[0] - boid.x, cohesion_vector[1] - boid.y]
            cohesion_vector = normalize_speed_limit(cohesion_vector, boid.Cons.MIN_LINEAR_SPEED, boid.Cons.MAX_LINEAR_SPEED)

        return cohesion_vector

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # separation rule: boids move away from other boids that are too close
    def separation_rule(self, boid, neighbors_positions):
        separation_vector = [0, 0]
        neighbor_sep_count = 0

        # calculate the sum of all neighbors positions
        for neighbor_pos in neighbors_positions:
            distance = calculate_distance(boid.position, neighbor_pos)
            if distance < boid.Cons.SEPARATION_RANGE:
                separation_vector[0] += neighbor_pos[0]
                separation_vector[1] += neighbor_pos[1]
                neighbor_sep_count += 1

        if neighbor_sep_count > 0:
            # calculate the average of the previous sum
            separation_vector[0] /= neighbor_sep_count
            separation_vector[1] /= neighbor_sep_count

            # steering away position = current_position - desired_position
            separation_vector = [boid.x - separation_vector[0], boid.y - separation_vector[1]]
            separation_vector = normalize_speed_limit(separation_vector, boid.Cons.MIN_LINEAR_SPEED, boid.Cons.MAX_LINEAR_SPEED)

        return separation_vector

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # obstacle avoidance rule: boids move away from obstacles that are too close
    def obstacle_avoidance_rule(self, boid):
        obstacle_avoidance_vector = [0, 0]
        obstacle_avoidance_count = 0

        # Skip lidar work and append the global obstacle positions [x,y] to the list
        # boid.Cons.OBSTACLES_POSITIONS = boid.Cons.OBSTACLES_POSITIONS

        # Calculate the sum of all neighbor obstacle positions
        for obstacle_pos in boid.Cons.OBSTACLES_POSITIONS:
            distance = calculate_distance(boid.position, obstacle_pos)
            # If there is an obstacle close to the boid by boid.Cons.CELL_SIZE or boid.Cons.OBSTACLE_AVOIDANCE_RANGE distance
            if distance < max(boid.Cons.CELL_SIZE, boid.Cons.OBSTACLE_AVOIDANCE_RANGE):
                # Mark this cell as an obstacle in ufco_matrix
                self.update_ufco_matrix_obstacles(boid, obstacle_pos)

            if distance < boid.Cons.OBSTACLE_AVOIDANCE_RANGE:
                obstacle_avoidance_vector[0] += obstacle_pos[0]
                obstacle_avoidance_vector[1] += obstacle_pos[1]
                obstacle_avoidance_count += 1

        if obstacle_avoidance_count > 0:
            # Calculate the average of the the previous sum
            obstacle_avoidance_vector[0] /= obstacle_avoidance_count
            obstacle_avoidance_vector[1] /= obstacle_avoidance_count

            # Steering away position = current_position - desired_position
            obstacle_avoidance_vector = [boid.x - obstacle_avoidance_vector[0], boid.y - obstacle_avoidance_vector[1]]

            # Normalize the obstacle_avoidance_vector
            obstacle_avoidance_vector = normalize_speed_limit(obstacle_avoidance_vector, boid.Cons.MIN_LINEAR_SPEED,boid.Cons.MAX_LINEAR_SPEED)


        return obstacle_avoidance_vector

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # wall avoidance rule: prevent boids from get out of work space
    # Bounding the position
    #   - In order to keep the flock within a certain area (eg. to keep them on-screen) Rather than unrealistically placing them within some confines and thus bouncing off invisible walls,
    #   - we implement a rule which encourages them to stay within rough boundaries. That way they can fly out of them, but then slowly turn back, avoiding any harsh motions.
    def wall_avoidance_rule(self, boid):
        # Initialize the wall avoidance vector
        wall_avoidance_vector = [0, 0]

        # Set the TURN_FACTOR to the maximum speed of the boid
        TURN_FACTOR = boid.Cons.MAX_LINEAR_SPEED    # The maximum speed of the boid

        # If the boid is close to the LEFT_WALL_X, steer it away from the wall by increasing its x position
        if boid.x < 0 + boid.Cons.WALL_AVOIDANCE_RANGE:  # move to right
            wall_avoidance_vector[0] += TURN_FACTOR
        # If the boid is close to the RIGHT_WALL_X, steer it away from the wall by decreasing its x position
        elif boid.x > boid.Cons.ARENA_WIDTH - boid.Cons.WALL_AVOIDANCE_RANGE:  # move to left
            wall_avoidance_vector[0] -= TURN_FACTOR
        # If the boid is close to the WALL_Y, steer it away from the wall by decreasing its y position
        elif boid.y > boid.Cons.ARENA_LENGTH - boid.Cons.WALL_AVOIDANCE_RANGE:
            wall_avoidance_vector[1] -= TURN_FACTOR
        # If the boid is close to the WALL_Y, steer it away from the wall by increasing its y position
        elif boid.y < 0 + boid.Cons.WALL_AVOIDANCE_RANGE:
            wall_avoidance_vector[1] += TURN_FACTOR

        # If the wall avoidance vector is not zero, normalize it
        if wall_avoidance_vector != [0, 0]:
            wall_avoidance_vector = normalize_speed_limit(wall_avoidance_vector, boid.Cons.MIN_LINEAR_SPEED, boid.Cons.MAX_LINEAR_SPEED)

        # Return the wall avoidance vector
        return wall_avoidance_vector


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Frontier rule: boids move toward the center of target Frontier point
    def frontier_rule(self, boid):
        frontier_vector = [0, 0]
        frontier_position = None     # Refers to no frontier

        # Search for target frontier point
        frontier_position = self.frontier_cell_search(boid)

        if frontier_position is not None:
            # Steering toward position = desired_position - current_position
            frontier_vector = [frontier_position[0] - boid.x, frontier_position[1] - boid.y]
            frontier_vector = normalize_speed_limit(frontier_vector, boid.Cons.MIN_LINEAR_SPEED, boid.Cons.MAX_LINEAR_SPEED)

        return frontier_vector
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to check surrounding frontiers for this boid and return position of the closest frontier cell
    def frontier_cell_search(self, boid):
        # Initialize the closest frontier cell position with None
        closest_frontier_cell_position = None     # Refers to no frontier

        # Check if the frontiers_list is not empty
        if boid.frontiers_list:
            # Initialize the closest distance with infinity
            closest_distance = float('inf')

            # Check frontiers_list cells to find the closest frontier cell position
            for frontier_cell in boid.frontiers_list:
                # Get the center position of the current frontier_cell
                frontier_cell_center = [(frontier_cell[1] + 0.5) * boid.Cons.CELL_SIZE, (frontier_cell[0] + 0.5) * boid.Cons.CELL_SIZE]
                # Calculate the distance between the frontier_cell_center and boid_position
                distance = calculate_distance(boid.position, frontier_cell_center)

                # If distance is less than the previous closest_distance, then update closest_frontier_cell_position
                if distance < closest_distance:
                    closest_frontier_cell_position = frontier_cell_center
                    closest_distance = distance

        return closest_frontier_cell_position
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    def update_surrounding_cells_as_frontiers(self, boid, cell_row, cell_col):
        # surrounding_cells in directions: up, down, left, right
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni = cell_row + di
            nj = cell_col + dj
            # If the surrounding cell is in ufco_matrix boundaries and is unexplored
            if 0 <= ni < boid.ufco_matrix_rows and 0 <= nj < boid.ufco_matrix_columns and boid.ufco_matrix[ni][nj] == 0:
                boid.ufco_matrix[ni][nj] = 1  # Mark this cell as frontier

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to update ufco_matrix with values 3 representing obstacle cell
    def update_ufco_matrix_obstacles(self, boid, obstacle_position):
        # Determine the current cell indices (row,col) in which the obstacle is located using obstacle position
        cell_row = math.floor(obstacle_position[1]/boid.Cons.CELL_SIZE)
        cell_col = math.floor(obstacle_position[0]/boid.Cons.CELL_SIZE)

        # Check if the obstacle is still in the boundary of the environment
        if (0 <= cell_row < boid.ufco_matrix_rows) and (0 <= cell_col < boid.ufco_matrix_columns):

            # if this cell is (unexplored or frontier), Then mark it as (obstacle)
            if boid.ufco_matrix[cell_row][cell_col] <= 2:
                boid.ufco_matrix[cell_row][cell_col] = 3

                # Update the four surrounding cells of the current cell with value 1 to represent frontiers
                self.update_surrounding_cells_as_frontiers(boid, cell_row, cell_col)
