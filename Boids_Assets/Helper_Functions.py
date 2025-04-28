"""
Helper Functions

This code snippet defines various utility functions that can be used for different purposes.
These functions cover a range of tasks such as normalizing angles and velocities, and calculate_distance.

@ Author            Reda Ghanem
@ Version           1.0
@ Last update       11/11/2023
"""

# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ********************  importing libraries and classes  ************************ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #

# [1]- importing libraries
import math                         # for mathematical operations
import os                           # for operating system related functionalities
import platform                     # Module for obtaining the operating system information
import sys                          # Module for interacting with the Python interpreter
import socket                       # for socket communication
import tkinter as tk                # Import the tkinter module and alias it as "tk"
from tkinter import messagebox


# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #

# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
# ┃------------------------- # Helper Functions  # ----------------------------┃ #
# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function takes a string as input and saves it to a text file in the current directory
def save_string_to_file_and_prompt_message(text, filename):
    # Get the current directory
    current_directory = os.getcwd()

    # Generate the file path
    file_path = os.path.join(current_directory, filename)

    # Open the file in write mode
    with open(file_path, 'w') as file:
        # Write the string to the file
        file.write(text)

    # Display the message box
    display_message(messagebox_title = filename, message = text)

    # Print a message to confirm the file has been saved
    # print("String has been saved to", file_path)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to display a GUI message in Python without using any external libraries
def display_message(messagebox_title = "Message Title", message = "Message Content"):
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Display the message box
    messagebox.showinfo(messagebox_title, message)

    # Start the Tkinter event loop
    root.mainloop()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to print a 2D matrix of integers in a nice format
def print_matrix(matrix, UFCO_MATRIX_COLUMNS):
    color_mapping = {
        0: '\033[47m',  # White background
        1: '\033[41m',  # Bright Red background
        2: '\033[42m',  # Green background
        3: '\033[44m',  # Blue background
    }

    print( "----" * UFCO_MATRIX_COLUMNS)
    
    for row in reversed(matrix):
        for value in row:
            value_str = str(int(value)).center(3)           # To center-align the values in the matrix while printing
            print(f"{color_mapping[value]}{value_str}\033[0m", end="|")
        print()
        print( "----" * UFCO_MATRIX_COLUMNS)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to map location [x, y, z] from Webots value to new value where (0,0) in left bottun courner
def get_translation_after_offset_back(translation, GPS_OFFSET_X , GPS_OFFSET_Y):
    # Apply offset to translation values to make all x and y positive so (x=0, y=0) in left bottom corner
    translation[0] -= GPS_OFFSET_X
    translation[1] -= GPS_OFFSET_Y
    translation = [translation[0]  , translation[1]  , translation[2]]
    return translation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to map from cell number(row,col) where (0,0) in Top left corner, to my offset webots position (x, y) where (0,0) in Bottom left corner
def map_from_row_col_to_position_xy(ROW_COL_POSITIONS, CELL_SIZE):
    X_Y_POSITIONS = [0] * len(ROW_COL_POSITIONS)

    for i in range(len(ROW_COL_POSITIONS)):
        row = ROW_COL_POSITIONS[i][0] - 1       # because in input file (row,col) start from (1,1) and we need to make it from (0,0)
        col = ROW_COL_POSITIONS[i][1] - 1       # because in input file (row,col) start from (1,1) and we need to make it from (0,0)
        x = col * CELL_SIZE + CELL_SIZE / 2     # note when we increse col we increse X-Axis
        y = row * CELL_SIZE + CELL_SIZE / 2     # note when we increse row we increse Y-Axis
        X_Y_POSITIONS[i] = [x, y]               # update X_Y_POSITIONS

    return X_Y_POSITIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to map from cell number(row,col) where (0,0) in Top left corner, to (row,col) where (0,0) in Bottom left corner
def map_row_col_from_top_left_to_bottom_left(ROW_COL_POSITIONS, TOTAL_ROWS):
    NEW_ROW_COL_POSITIONS = [0] * len(ROW_COL_POSITIONS)

    for i in range(len(ROW_COL_POSITIONS)):
        row = ROW_COL_POSITIONS[i][0]        # because in input file (row,col) start from (1,1) and we need to make it from (0,0)
        col = ROW_COL_POSITIONS[i][1]        # because in input file (row,col) start from (1,1) and we need to make it from (0,0)
        new_row = TOTAL_ROWS - row + 1       # +1 to make (16-1) + 1 = 16
        new_col = col
        NEW_ROW_COL_POSITIONS[i] = [new_row, new_col]               # update row and col

    return NEW_ROW_COL_POSITIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to map from cell number(row,col) where (0,0) in Bottom left corner, to (row,col) where (0,0) in Top left corner
def map_row_col_from_bottom_left_to_top_left(ROW_COL_POSITIONS, TOTAL_ROWS):
    NEW_ROW_COL_POSITIONS = [0] * len(ROW_COL_POSITIONS)

    for i in range(len(ROW_COL_POSITIONS)):
        row = ROW_COL_POSITIONS[i][0]        # because in input file (row,col) start from (1,1) and we need to make it from (0,0)
        col = ROW_COL_POSITIONS[i][1]        # because in input file (row,col) start from (1,1) and we need to make it from (0,0)
        new_row = TOTAL_ROWS - row + 1       # +1 to make (16-1) + 1 = 16
        new_col = col
        NEW_ROW_COL_POSITIONS[i] = [new_row, new_col]               # update row and col

    return NEW_ROW_COL_POSITIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to map from position (x,y) where (0,0) in Bottom left corner, to (x,y) where (0,0) in Top left corner
def map_x_y_from_bottom_left_to_top_left(x, y, DISPLAY_GROUND_HEIGHT):
    
    y = DISPLAY_GROUND_HEIGHT - y
    NEW_X_Y_POSITIONS = [x, y]               # update row and col

    return NEW_X_Y_POSITIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to writes a list of data to a file and saves the file
def write_list_to_file(file_path, data):
    with open(file_path, 'w') as file:
        for item in data:
            file.write(str(item) + ' ')

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to extract the robot ID from the robot name format Pioneer 3-DX(ID), where ID can be any positive integer
def extract_robot_id(robot_name):
    start_index = robot_name.find('(') + 1
    end_index = robot_name.find(')')
    if start_index > 0 and end_index > start_index:
        robot_id_str = robot_name[start_index:end_index]
        try:
            robot_id = int(robot_id_str)
            return robot_id - 1
        except ValueError:
            return None
    else:
        return None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to get GPS values after applying offset
def get_GPS_values_after_offset(gps, GPS_OFFSET_X, GPS_OFFSET_Y):
    robot_position = gps.getValues()        # get current position
    # Apply offset to GPS values to make all x and y positive so (x=0, y=0) in left bottom corner
    robot_position[0] += GPS_OFFSET_X
    robot_position[1] += GPS_OFFSET_Y
    robot_position = [robot_position[0]  , robot_position[1]  , robot_position[2]]

    # Comment this for now: to correct the GPS offset numbers in x,y,z , because GPS return number not as expected in world points
    # robot_position = [robot_position[0] + 0.15069182145 , robot_position[1] + 0.06543356919 , robot_position[2]]
    
    robot_position = robot_position[:2]             # we just need x, y and ignore z
    return robot_position
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to get heading angle
def get_heading_angle(compass):
    robot_compass_values = compass.getValues()
    heading_angle = math.atan2(robot_compass_values[0], robot_compass_values[1])
    return heading_angle

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to normalize the difference between two angles
def normalize_angle_diff(angle_diff):
    angle_diff = math.atan2(math.sin(angle_diff) , math.cos(angle_diff))

    # round values to make numbers same in all OS (Windows, Linux)
    angle_diff = round(angle_diff, 5)

    return angle_diff
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to normalize the angular velocity vector
def normalize_angular_velocity(raw_angular_velocity, min_angular_speed, max_angular_speed):
    clamped_angular_velocity = max(min(raw_angular_velocity, max_angular_speed), min_angular_speed)

    # round values to make numbers same in all OS (Windows, Linux)
    clamped_angular_velocity = round(clamped_angular_velocity, 5)

    return clamped_angular_velocity
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to normalize the linear speed vector
def normalize_speed_limit(speed , min_speed , max_speed ):
    speed_magnitude = math.sqrt(speed[0]**2 + speed[1]**2)
    if speed_magnitude != 0:
        if speed_magnitude > max_speed:
            speed[0] = (speed[0] / speed_magnitude) * max_speed
            speed[1] = (speed[1] / speed_magnitude) * max_speed
        elif speed_magnitude < min_speed:
            speed[0] = (speed[0] / speed_magnitude) * min_speed
            speed[1] = (speed[1] / speed_magnitude) * min_speed
    
    # round values to make numbers same in all OS (Windows, Linux)
    speed = [round(v, 5) for v in [speed[0], speed[1]] ]
    
    return speed
# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
def calculate_distance(point_a, point_b):
        # Calculate the difference between point_a and point_b
        distance_diff = [point_a[0] - point_b[0], point_a[1] - point_b[1]]
        # Calculate the Euclidean distance using the distance difference
        distance = math.sqrt(distance_diff[0] ** 2 + distance_diff[1] ** 2)

        # round values to make numbers same in all OS (Windows, Linux)
        # distance = round(distance, 5)
    
        return distance
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to calculate the wheel velocities based on linear and angular velocities
def calculate_wheel_velocities(linear_velocity, angular_velocity, WHEEL_DISTANCE, WHEEL_RADIUS):
    left_wheel_velocity =  ( (2*linear_velocity) - (angular_velocity * WHEEL_DISTANCE) ) / (2 * WHEEL_RADIUS)
    right_wheel_velocity = ( (2*linear_velocity) + (angular_velocity * WHEEL_DISTANCE) ) / (2 * WHEEL_RADIUS)

    # round values to make numbers same in all OS (Windows, Linux)
    left_wheel_velocity = round(left_wheel_velocity, 5)
    right_wheel_velocity = round(right_wheel_velocity, 5)
    
    return left_wheel_velocity, right_wheel_velocity
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to rotate a 2D vector by a specified angle
def rotate_vector(vector, angle):
    # Convert the angle from degrees to radians
    angle_rad = math.radians(angle)
    # Calculate the cosine and sine values of the angle
    cos_val = math.cos(angle_rad)
    sin_val = math.sin(angle_rad)
    # Perform the rotation transformation on the vector using the rotation matrix
    rotated_vector = [cos_val*vector[0] - sin_val*vector[1], sin_val*vector[0] + cos_val*vector[1]]

    # round values to make numbers same in all OS (Windows, Linux)
    rotated_vector = [round(v, 5) for v in [rotated_vector[0], rotated_vector[1]] ]

    # Return the rotated vector
    return rotated_vector
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to print a 2D matrix of integers in a nice format
def print_matrix(matrix, UFCO_MATRIX_COLUMNS):
    color_mapping = {
        0: '\033[47m',  # White background
        1: '\033[41m',  # Bright Red background
        2: '\033[42m',  # Green background
        3: '\033[44m',  # Blue background
    }

    print("UFCO_MATRIX:")
    print( "----" * UFCO_MATRIX_COLUMNS)
    
    for row in reversed(matrix):
        for value in row:
            value_str = str(int(value)).center(3)           # To center-align the values in the matrix while printing
            print(f"{color_mapping[value]}{value_str}\033[0m", end="|")
        print()
        print( "----" * UFCO_MATRIX_COLUMNS)
# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
# Function to disable printing to standard output
def disable_print():
    # Redirect the standard output to os.devnull
    sys.stdout = open(os.devnull, 'w')
# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
# Clear the console based on the operating system
def clear_console():
    if platform.system() == 'Windows':
        os.system('cls')  # Clear console for Windows
    else:
        os.system('clear')  # Clear console for Unix-like systems
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function receives a folder path and file extension format,
# reads all the files with that extension in the folder, and returns a dictionary
def load_from_folder(folder_path, extension):
    dictionary = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(extension):
            file_path = os.path.join(folder_path, filename)
            file_name = os.path.splitext(filename)[0]

            # Add the font_path to the dictionary
            dictionary[file_name] = file_path

    return dictionary
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
def is_port_available(server_host , port_number):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Try binding to the specified port
        sock.bind((server_host, port_number))

        # Port is available
        sock.close()
        print(f"Port {port_number} is available.")
        return True
    except OSError:
        # Port is not available
        print(f"Port {port_number} is not available.")
        return False
    
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to round recived value (single number and list) to 5 decimals
def round_value_to_5_decimals(value):

    # If the input is a float, round it to 5 decimal places and return the result
    if isinstance(value, (float)):
        return round(value, 5)
    # If the input is a list, create a new list where each element is rounded to 5 decimal places
    elif isinstance(value, list):
        return [round(v, 5) for v in value]
    # If the input is an integer, return it as is
    elif isinstance(value, (int)):
        return value
    # If the input is neither a number nor a list, raise a ValueError with an error message
    else:
        raise ValueError("round_to_5_decimals: Input must be a number or a list of numbers")