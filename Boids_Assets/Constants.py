"""
Constants Class

This section of the code handles the initialization and configuration of various parameters and settings for a simulation environment.
It encompasses the loading of configuration data from a JSON file, setting up constants and variables, and preparing the simulation environment.

@ Author            Reda Ghanem
@ Version           1.0
@ Last update       11/11/2023
"""



# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ********************  importing libraries and classes  ************************ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #

# [1]- importing libraries
import json                         # for JSON handling
import sys, os                      # to obtain the current path and Set working directory to current_directory


# [2]- very important if you want to access all files and Modules from current_directory
# Get the current directory and append it to the system path
current_directory, filename = os.path.split(os.path.abspath(__file__))  # Get the current directory of the current file
sys.path.append(current_directory)                                      # Append the current directory to the system path

# [3]- importing Classes and Functions
from .Helper_Functions import *     # for helper functions

# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #



# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
# ┃-------------------------- # Constants Class # -----------------------------┃ #
# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
class Constants:

    def __init__(self, behaviors_weights_ranges_from_tunable_parameters=None, print_tunable_parameters_status=True, GUI_flag = True):
        # Initialize your constants here
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
        # *********************      Initialization     ****************************** #
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #

        SWARMING_RUN_ON = "Python_Simulation"

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #


        # Load data from the Configuration.json JSON file,
        configuration_json_file_path = os.path.join(current_directory,'Configuration.json')  # Path to the Configuration.json JSON file
        with open(configuration_json_file_path, 'r') as json_file:
            loaded_data = json.load(json_file)

        # Extract the values from the JSON data and store them in variables
        # Behaviors Weights, numbers in range [0,1]
        self.ALIGNMENT_WEIGHT = loaded_data['ALIGNMENT_WEIGHT']
        self.COHESION_WEIGHT = loaded_data['COHESION_WEIGHT']
        self.SEPARATION_WEIGHT = loaded_data['SEPARATION_WEIGHT']
        self.OBSTACLE_AVOIDANCE_WEIGHT = loaded_data['OBSTACLE_AVOIDANCE_WEIGHT']
        self.WALL_AVOIDANCE_WEIGHT = loaded_data['WALL_AVOIDANCE_WEIGHT']
        self.FRONTIER_WEIGHT = loaded_data['FRONTIER_WEIGHT']
        # Behaviors Range, All Next Distance in meter, numbers in range [0, Max range for the Emitter and Receiver]
        self.ALIGNMENT_RANGE = loaded_data['ALIGNMENT_RANGE']
        self.COHESION_RANGE = loaded_data['COHESION_RANGE']
        self.SEPARATION_RANGE = loaded_data['SEPARATION_RANGE']
        self.OBSTACLE_AVOIDANCE_RANGE = loaded_data['OBSTACLE_AVOIDANCE_RANGE']
        self.WALL_AVOIDANCE_RANGE = loaded_data['WALL_AVOIDANCE_RANGE']
        self.SHARE_RANGE = loaded_data['SHARE_RANGE']
        # Robot Speed
        self.MAX_LINEAR_SPEED = loaded_data['MAX_LINEAR_SPEED']                             # Maximium robot linear speed m/s
        self.MIN_LINEAR_SPEED = loaded_data['MIN_LINEAR_SPEED']                             # Minimum robot linear speed m/s
        self.MAX_ANGULAR_SPEED = loaded_data['MAX_ANGULAR_SPEED']                           # Maximium robot angular speed rad/s
        self.MIN_ANGULAR_SPEED = loaded_data['MIN_ANGULAR_SPEED']                           # Minimum robot angular speed rad/s
        # Environmental Setup
        self.ARENA_WIDTH = loaded_data['ARENA_WIDTH']                                       # RectangleArena Width, (in meters)
        self.ARENA_LENGTH = loaded_data['ARENA_LENGTH']                                     # RectangleArena Length, (in meters)
        self.CELL_SIZE = loaded_data['CELL_SIZE']                                           # Cell Size, (in meters)

        self.ROBOT_NAME = loaded_data['ROBOT_NAME']                                         # robot name: Pioneer_3DX or RVR
        self.NUM_OF_ROBOTS = loaded_data['NUM_OF_ROBOTS']                                   # Number of robots
        self.ROBOTS_ROW_COL = loaded_data["ROBOTS_ROW_COL"]                                 # initia robots positions in term of (row,col)
        self.NUM_OF_OBSTACLES = loaded_data['NUM_OF_OBSTACLES']                             # number of obstacles
        self.OBSTACLES_ROW_COL = loaded_data["OBSTACLES_ROW_COL"]                           # initial obstacles positions in term of (row,col)

        self.ITERATIONS_PER_SECOND = loaded_data['ITERATIONS_PER_SECOND']                   # Number of iterations per second
        self.SAVE_ENVIRONMENT_UPDATES_TO = loaded_data['SAVE_ENVIRONMENT_UPDATES_TO']       # name of file to save updates of webots world if exist

        self.MAX_STOP_TIME = loaded_data['MAX_STOP_TIME']                                   # Stop simulation after ... sec
        self.FBS = loaded_data['FBS']                                                       # Frame per second
        self.DISPLAY_GROUND_MOD = loaded_data['DISPLAY_GROUND_MOD']                         # Enable coloring ground if True
        self.RENDERING = loaded_data['RENDERING']  # Enable GUI if True
        self.PRINT_CONSOLE_RESULT = loaded_data["PRINT_CONSOLE_RESULT"]                     # print results in console if true
        self.SPEED_OF_SIMULATION = loaded_data["SPEED_OF_SIMULATION"]                       # SPEED_OF_SIMULATION 1,2,3,..., 10

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #

        # check if we have Behaviors_Weights_Ranges_from_Optimization
        if behaviors_weights_ranges_from_tunable_parameters is not None:
            if print_tunable_parameters_status == True:
                print("This simulation will run with Behaviors_Weights_Ranges_from (tunable_parameters)", behaviors_weights_ranges_from_tunable_parameters)
            # update Behaviors Weights and Ranges from tunable_parameters
            self.update_behaviors_weights_ranges_from_tunable_parameters(behaviors_weights_ranges_from_tunable_parameters)
            self.RENDERING = GUI_flag                       # if GUI_flag is True, then we will use GUI, otherwise we will not use GUI
        else:
            if print_tunable_parameters_status == True:
                print("This simulation will run with Behaviors_Weights_Ranges_from (Configuration.json)")

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
        # Robot body dimensions
        if self.ROBOT_NAME == "Pioneer_3DX":
            self.robot_width  = 0.381   # Width of Pioneer 3DX (in meters)
            self.robot_length = 0.458   # Length of Pioneer 3DX (in meters)
            self.robot_height = 0.217   # Height of Pioneer 3DX (in meters)

            self.WHEEL_RADIUS = 0.09765  # Radius of Pioneer 3DX wheel (in meters)
            self.WHEEL_DISTANCE = 0.33  # Distance between wheels of Pioneer 3DX (in meters)

        elif self.ROBOT_NAME == "RVR":
            self.robot_width  = 0.216   # Width of RVR (in meters)
            self.robot_length = 0.185   # Length of RVR (in meters)
            self.robot_height = 0.114   # Height of RVR (in meters)

        # set Robot size in meters
        self.ROBOT_SIZE = [self.robot_width, self.robot_length]  # make ROBOT_SIZE in cm and int
        # calculate the radius of the circle that can contain the robot
        diagonal_of_robot = math.sqrt(self.ROBOT_SIZE[0] ** 2 + self.ROBOT_SIZE[1] ** 2)    # Diagonal of the robot
        self.ROBOT_RADIUS = 0.5 * diagonal_of_robot                                         # Radius of the circle that can contain the robot

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
        # Variables for Area Coverage Problem
        self.UFCO_MATRIX_ROWS = int(self.ARENA_LENGTH / self.CELL_SIZE)  # note when we increse ARENA_LENGTH rows incresed
        self.UFCO_MATRIX_COLUMNS = int(self.ARENA_WIDTH / self.CELL_SIZE)  # note when we increse ARENA_WIDTH column incresed
        self.TOTAL_CELLS = self.UFCO_MATRIX_ROWS * self.UFCO_MATRIX_COLUMNS  # Total number of cells

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
        # We need to make some adjustments based on the value of variable SWARMING_RUN_ON

        self.ROBOTS_POSITIONS = None            # to get ROBOTS_POSITIONS (x, y) from ROBOTS_ROW_COL
        self.OBSTACLES_POSITIONS = None         # to get OBSTACLES_POSITIONS (x, y) from ROBOTS_ROW_COL

        if SWARMING_RUN_ON == "Real_Environment" or SWARMING_RUN_ON == "Webots_Simulation":

            # Make all positions positive by adding the offset to make the original point (0,0) at the bottom left corner
            self.GPS_OFFSET_X = self.ARENA_WIDTH / 2  # Width of RectangleArena/2
            self.GPS_OFFSET_Y = self.ARENA_LENGTH / 2  # Length of RectangleArena/2

            # for Server messages length
            self.SINGLE_MESSAGE_LENGTH = 5 + (self.UFCO_MATRIX_ROWS * self.UFCO_MATRIX_COLUMNS)  # single message consist of: "{id},{x},{y},{delta_x},{delta_y,{ufco_matrix}"

            # update values from (row,col) to position (x, y) where (0,0) in the bottom left corner
            self.ROBOTS_ROW_COL = map_row_col_from_top_left_to_bottom_left(self.ROBOTS_ROW_COL, self.UFCO_MATRIX_ROWS)
            self.ROBOTS_POSITIONS = map_from_row_col_to_position_xy(self.ROBOTS_ROW_COL, self.CELL_SIZE)

            # update values from (row,col) to webots position (x, y) where (0,0) in the bottom left corner
            self.OBSTACLES_ROW_COL = map_row_col_from_top_left_to_bottom_left(self.OBSTACLES_ROW_COL, self.UFCO_MATRIX_ROWS)
            self.OBSTACLES_POSITIONS = map_from_row_col_to_position_xy(self.OBSTACLES_ROW_COL, self.CELL_SIZE)
        else:
            self.apply_adjustments_for_simulation_on_python()




    # ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
    # ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
    # ┃-------------------------- # For Optimization # ----------------------------┃ #
    # ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
    # ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #

    # Function to update Behaviors Weights and Ranges from tunable_parameters
    def update_behaviors_weights_ranges_from_tunable_parameters(self, tunable_parameters=[]):

        # Checking if tunable_parameters length is correct
        if len(tunable_parameters) != 12:
            print("tunable parameters length must equal 12: (6 float, 6 int) ")
            print("tunable parameters values must be in centimeter and ranges for Behaviors Weights [0,1] and Behaviors Range [0, max_Emitter_Range]")
            return

        # Behaviors Weights, numbers in range [0,1] received from optimization code
        self.ALIGNMENT_WEIGHT = float(tunable_parameters[0])
        self.COHESION_WEIGHT = float(tunable_parameters[1])
        self.SEPARATION_WEIGHT = float(tunable_parameters[2])
        self.OBSTACLE_AVOIDANCE_WEIGHT = float(tunable_parameters[3])
        self.WALL_AVOIDANCE_WEIGHT = float(tunable_parameters[4])
        self.FRONTIER_WEIGHT = float(tunable_parameters[5])

        # Behaviors Range, numbers in range [0,max_Emitter_Range] received from optimization code
        # Convert from Centimeter to maters,
        self.ALIGNMENT_RANGE = int(tunable_parameters[6])/100
        self.COHESION_RANGE = int(tunable_parameters[7])/100
        self.SEPARATION_RANGE = int(tunable_parameters[8])/100
        self.OBSTACLE_AVOIDANCE_RANGE = int(tunable_parameters[9])/100
        self.WALL_AVOIDANCE_RANGE = int(tunable_parameters[10])/100
        self.SHARE_RANGE = int(tunable_parameters[11])/100



    # ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
    # ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
    # ┃---------------------------- # For python # --------------------------------┃ #
    # ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
    # ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #

    def apply_adjustments_for_simulation_on_python(self):

        # Convert from maters to Centimeter, where we assume 1 pixel = 1 cm
        self.ALIGNMENT_RANGE                = int(self.ALIGNMENT_RANGE * 100)
        self.COHESION_RANGE                 = int(self.COHESION_RANGE * 100)
        self.SEPARATION_RANGE               = int(self.SEPARATION_RANGE * 100)
        self.OBSTACLE_AVOIDANCE_RANGE       = int(self.OBSTACLE_AVOIDANCE_RANGE * 100)
        self.WALL_AVOIDANCE_RANGE           = int(self.WALL_AVOIDANCE_RANGE * 100)
        self.SHARE_RANGE                    = int(self.SHARE_RANGE * 100)
        self.ARENA_WIDTH                    = int(self.ARENA_WIDTH * 100)
        self.ARENA_LENGTH                   = int(self.ARENA_LENGTH * 100)
        self.CELL_SIZE                      = int(self.CELL_SIZE * 100)

        # ANGULAR_SPEED need to divide by 100, to make change of ANGULAR_SPEED every 100 step correct as target value you want
        # for ex. if we want 0.9 rad/s this means that we need to use 0.009 so after 100 steps (one sec) we reach 0.9 rad/sec
        self.MAX_ANGULAR_SPEED = self.MAX_ANGULAR_SPEED / 100
        self.MIN_ANGULAR_SPEED = self.MIN_ANGULAR_SPEED / 100

        # Convert ROBOT_SIZE and ROBOT_RADIUS from maters to Centimeter,
        self.robot_width  = int(self.robot_width * 100)   # Width in Centimeter
        self.robot_length = int(self.robot_length * 100)  # Length in Centimeter
        self.robot_height = int(self.robot_height * 100)  # Height in Centimeter
        # set Robot size in Centimeter
        self.ROBOT_SIZE = [self.robot_width, self.robot_length]
        # calculate the radius of the circle that can contain the robot
        diagonal_of_robot = math.sqrt(self.ROBOT_SIZE[0] ** 2 + self.ROBOT_SIZE[1] ** 2)  # Diagonal of the robot
        self.ROBOT_RADIUS = 0.5 * diagonal_of_robot  # Radius of the circle that can contain the robot

        # Do this step again since we have CELL_SIZE in Centimeter now, and the original point (0,0) at top left corner
        self.ROBOTS_POSITIONS    = map_from_row_col_to_position_xy(self.ROBOTS_ROW_COL, self.CELL_SIZE)
        self.OBSTACLES_POSITIONS = map_from_row_col_to_position_xy(self.OBSTACLES_ROW_COL, self.CELL_SIZE)

