"""
Environment Class

This class represents the environment of the simulator and provides methods for drawing the window, robots, and results,
this class also provides methods for checking events and quitting the simulator.
this class show the results on the right surface, and draw the robots and the display ground on the left surface.


@ Author            Reda Ghanem
@ Version           1.0
@ Last update       11/11/2023
"""

# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ********************  importing libraries and classes  ************************ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #

# [1]- importing libraries
import pygame                       # for graphics and input handling
import sys, os                      # to obtain the current path and Set working directory to current_directory

# [2]- very important if you want to access all files and Modules from current_directory
# Get the current directory and append it to the system path
current_directory, filename = os.path.split(os.path.abspath(__file__))  # Get the current directory of the current file
sys.path.append(current_directory)                                      # Append the current directory to the system path

# [3]- importing Classes and Functions
from Boids_Assets.Helper_Functions import *

# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #


# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
# ┃------------------------- # Environment Class # ----------------------------┃ #
# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #

class Environment:
    def __init__(self, constants, recived_Performance_Metrics):

        self.Cons = constants  # receive Constants and Global variables from main code

        pygame.init()       # initialize pygame

        self.Performance_Metrics = recived_Performance_Metrics

        # ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
        # ┃----------------------------- # For GUI # ----------------------------------┃ #
        # ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
        self.SIMULATOR_ICON = os.path.join(current_directory, "Icon","Wheeled_Mobile_Robots_Simulator_3.png")  # Path to the folder containing the images
        # ROBOT SKINS images
        images_folder_path = os.path.join(current_directory,"Robot_Skins_Images")  # Path to the folder containing the images
        self.ROBOT_SKINS = load_from_folder(images_folder_path,".png")  # Get all .png files in the folder as dictionary
        # Fonts
        self.FONT_SIZE = int(self.Cons.CELL_SIZE / 2.5)  # font size to render the id on the robot
        fonts_folder_path = os.path.join(current_directory, "Fonts")  # Path to the folder containing the images
        self.FONTS = load_from_folder(fonts_folder_path, ".ttf")  # Get all .ttf files in the folder as dictionary

        self.RIGHT_SURFACE_WIDTH = 300  # right_surface for showing results, 300 cm = 300 pixels
        self.LINE_WIDTH = 1  # Define the line width for drawing rows and columns

        # Colors
        self.RGB_COLORS = RGB_COLORS()

        # ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
        # ┃----------------------- # Initialize the display # -------------------------┃ #
        # ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #

        pygame.event.pump()

        # MAP dimensions
        dimensions = (self.Cons.ARENA_WIDTH + self.RIGHT_SURFACE_WIDTH , self.Cons.ARENA_LENGTH)
        self.width, self.length = dimensions

        # window settings
        pygame.display.set_caption("Point Mass Robot Simulator - Reda Ghanem - UNSW")       # Set the window title
        icon_image = pygame.image.load(self.SIMULATOR_ICON)                                 # Load the icon image
        pygame.display.set_icon(icon_image)                                                 # Set the window icon
        self.window = pygame.display.set_mode( (self.width, self.length) )

        # Create left and right surfaces
        self.left_surface = pygame.Surface((self.Cons.ARENA_WIDTH, self.Cons.ARENA_LENGTH))
        self.right_surface = pygame.Surface((self.RIGHT_SURFACE_WIDTH, self.Cons.ARENA_LENGTH))

        self.draw_display_ground()


        # Buttons
        self.play_button_rect  = pygame.Rect(10 , self.Cons.ARENA_LENGTH - 80, 80, 30)
        self.pause_button_rect = pygame.Rect(100, self.Cons.ARENA_LENGTH - 80, 80, 30)
        self.reset_button_rect = pygame.Rect(190, self.Cons.ARENA_LENGTH - 80, 80, 30)

        self.play_button_enable = True
        self.pause_button_enable = False
        self.reset_button_enable = True




# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    def draw_window(self, robots, boids):

        # Draw display ground on the left surface
        self.draw_display_ground(boids)

        # Draw all robots on the left surface
        self.draw_robots(robots)

        # Display Results on the right surface
        self.draw_results()
        
        # Blit the left and right surfaces onto the main screen
        self.window.blit(self.left_surface, (0, 0))
        self.window.blit(self.right_surface, (self.Cons.ARENA_WIDTH, 0))

        pygame.display.update()
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    def draw_display_ground(self, boids = []):

        self.left_surface.fill(self.RGB_COLORS.black)        # Set the left_surface color to white

        # Draw rows lines
        for i in range(0, self.Cons.ARENA_LENGTH, self.Cons.CELL_SIZE):
            # Draw a horizontal line
            pygame.draw.line(self.left_surface, self.RGB_COLORS.black, (0, i ), (self.Cons.ARENA_WIDTH - 1, i), self.LINE_WIDTH)     # y move to draw rows

        # Draw columns lines
        for i in range(0, self.Cons.ARENA_WIDTH, self.Cons.CELL_SIZE):
            # Draw a vertical line from
            pygame.draw.line(self.left_surface, self.RGB_COLORS.black, (i , 0), (i , self.Cons.ARENA_LENGTH - 1), self.LINE_WIDTH)    # x move to draw columns


        # Copy GLOBAL_UFCO_MATRIX to the diplay ground
        for row in range (self.Cons.UFCO_MATRIX_ROWS):
            for col in range(self.Cons.UFCO_MATRIX_COLUMNS):
                if self.Performance_Metrics.GLOBAL_UFCO_MATRIX[row][col] == 0:
                    self.fill_square_with_color(row, col, self.RGB_COLORS.white)       # UnExplored
                elif self.Performance_Metrics.GLOBAL_UFCO_MATRIX[row][col] == 1:
                    self.fill_square_with_color(row, col, self.RGB_COLORS.orange)      # Frontier
                elif self.Performance_Metrics.GLOBAL_UFCO_MATRIX[row][col] == 2:
                    self.fill_square_with_color(row, col, self.RGB_COLORS.green)       # Explored
                elif self.Performance_Metrics.GLOBAL_UFCO_MATRIX[row][col] == 3:
                    self.fill_square_with_color(row, col, self.RGB_COLORS.blue)        # Obstacle


        # Step [04]: Draw a yellow line between any two connected robots
        for i, boid in enumerate(boids):
            
            # Check distance between current robot and the other_robot
            for other_boid in boids[i+1:]:
                distance = calculate_distance(boid.position, other_boid.position)
                # Check is this two robots connected or not
                if distance < self.Cons.SHARE_RANGE:
                    # Draw a yellow line between any two robots within share range R_sh
                    robot_position_x_y = [int(boid.position[0]), int(boid.position[1])]
                    other_robot_position_x_y = [int(other_boid.position[0]), int(other_boid.position[1])]
                    pygame.draw.line(self.left_surface, self.RGB_COLORS.yellow, (robot_position_x_y[0], robot_position_x_y[1]), (other_robot_position_x_y[0] , other_robot_position_x_y[1]) , self.LINE_WIDTH)

        
        # Step [05]: Draw Circle arround first robot, which have id = 0
        for i, boid in enumerate(boids):

            # Draw Ranges, each range (R_𝑎, R_𝑐, R_𝑠, R_𝑎𝑣, R_𝑤, R_𝑠ℎ) represented by circle around the robot with id 0
            if boid.id == 0:
                ranges_and_colors = {
                    self.Cons.ALIGNMENT_RANGE:            self.RGB_COLORS.black,
                    self.Cons.COHESION_RANGE:             self.RGB_COLORS.red,
                    self.Cons.SEPARATION_RANGE:           self.RGB_COLORS.purple,
                    self.Cons.OBSTACLE_AVOIDANCE_RANGE:   self.RGB_COLORS.magenta,
                    self.Cons.WALL_AVOIDANCE_RANGE:       self.RGB_COLORS.cyan,
                    self.Cons.SHARE_RANGE:                self.RGB_COLORS.olive
                }

                robot_position_x_y = [int(boid.position[0] ), int(boid.position[1] )] 

                for range_value, color in ranges_and_colors.items():
                    horizontal_and_vertical_radius = range_value 
                    pygame.draw.circle(self.left_surface, color, (robot_position_x_y[0], robot_position_x_y[1]), horizontal_and_vertical_radius , self.LINE_WIDTH)


                    
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to fill a square in position (row, col) with color
    def fill_square_with_color(self, row, col, color):
        position_x = int(col * self.Cons.CELL_SIZE)
        position_y = int(row * self.Cons.CELL_SIZE)

        margin = self.LINE_WIDTH
        pygame.draw.rect(self.left_surface, color, (position_x + margin, position_y + margin, self.Cons.CELL_SIZE - margin, self.Cons.CELL_SIZE - margin))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to draw all robots on the left surface
    def draw_robots(self, robots):
        # Create a black circle surface
        circle_radius = int(self.FONT_SIZE / 2.5)
        circle_surface = pygame.Surface((circle_radius * 2, circle_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, (0, 0, 0), (circle_radius, circle_radius), circle_radius)

        # Create a font object to render the id on the robot
        font = pygame.font.Font(None, self.FONT_SIZE)

        # Draw all robots on the left surface
        for robot in robots:
            original_img = pygame.image.load(robot.robot_img_path)                                            # Load the original image
            image = pygame.transform.scale(original_img, (robot.boid.radius*2, robot.boid.radius*2))     # Scale the image
            rotated = pygame.transform.rotozoom(image, math.degrees(-robot.boid.heading_angle),1)       # Rotate the image
            rectangle = rotated.get_rect(center=(int(robot.boid.x), int(robot.boid.y)))                       # Get the rectangle of the rotated image
            robot_surface = rotated                                                                           # Set the robot surface to the rotated image
            robot_position = rectangle                                                                        # Set the robot position to the rectangle

            # Calculate the position for the circle and text
            circle_position = (int(robot.boid.x) - circle_radius, int(robot.boid.y) - circle_radius)
            text = font.render(str(robot.boid.id), True, (255, 255, 255))
            text_position = (circle_position[0] + circle_radius - text.get_width() // 2,
                             circle_position[1] + circle_radius - text.get_height() // 2)

            # Blit the rotated image, circle, and text onto the left surface
            self.left_surface.blit(robot_surface, robot_position)                       # Draw robot on the left surface
            self.left_surface.blit(circle_surface, circle_position)                     # Draw circle on the left surface
            self.left_surface.blit(text, text_position)                                 # Draw text on the left surface

        
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    def draw_results(self):

        # Display Results on the right surface
        self.right_surface.fill(self.RGB_COLORS.Turquoise)         # Set the right_surface color
        font = pygame.font.Font(self.FONTS["Arial"], 15)


        text_position = [10, 10]     # [10, 10] starting from right_surface
        self.add_text(self.right_surface, font, f"Experiment Runtime {' '*3}= {self.Performance_Metrics.EXPERIMENT_RUNTIME:05.2f} Seconds", text_position)
        text_position[1] += 30

        self.add_text(self.right_surface, font, f"Covered Cells {' '*13}= {self.Performance_Metrics.COVERAGE_COUNT}/{self.Cons.TOTAL_CELLS}", text_position)
        text_position[1] += 30

        # Add Line
        text_position[1] += 10
        pygame.draw.line(self.right_surface, self.RGB_COLORS.black, text_position, (text_position[0] + self.RIGHT_SURFACE_WIDTH, text_position[1]), self.LINE_WIDTH)
        text_position[1] += 20

        # Performance Metrics
        font.set_bold(True)             # Set the font to bold
        self.add_text(self.right_surface, font, f"Performance Metrics {' ' * 10}", text_position)
        text_position[1] += 30
        font.set_bold(False)            # Set the font to normal again

        # VIOLATIONS
        self.add_text(self.right_surface, font, f"Violations {' '*20}= {self.Performance_Metrics.VIOLATIONS:05.2f}", text_position)
        text_position[1] += 30

        # COVERAGE_PERCENTAGE
        self.add_text(self.right_surface, font, f"Coverage Percentage = {self.Performance_Metrics.COVERAGE_PERCENTAGE:05.2f}%", text_position)
        text_position[1] += 30

       

        # TURNAROUND_TIME
        self.add_text(self.right_surface, font, f"Turnaround Time {' '*8}= {self.Performance_Metrics.TURNAROUND_TIME:05.2f} Seconds", text_position)
        text_position[1] += 30

        # Add Line
        text_position[1] += 10
        pygame.draw.line(self.right_surface, self.RGB_COLORS.black, text_position, (text_position[0] + self.RIGHT_SURFACE_WIDTH, text_position[1]), self.LINE_WIDTH)
        text_position[1] += 20


        # Draw buttons
        # Draw the play button
        self.add_button(self.right_surface, self.play_button_rect, self.RGB_COLORS.green, "Play", font, self.play_button_enable)

        # Draw the pause button
        self.add_button(self.right_surface, self.pause_button_rect, self.RGB_COLORS.orange, "Pause", font, self.pause_button_enable)

        # Draw the reset button
        self.add_button(self.right_surface, self.reset_button_rect, self.RGB_COLORS.red, "Reset", font, self.reset_button_enable)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    def check_event(self):
        event = pygame.event.poll()  # Get the current event
        
        if event.type == pygame.QUIT:
            print("QUIT button clicked")
            return "QUIT"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                if self.play_button_rect.collidepoint(event.pos[0] - self.Cons.ARENA_WIDTH, event.pos[1]) and self.play_button_enable:
                    print("Play button clicked")
                    self.play_button_enable = False
                    self.pause_button_enable = True
                    return "Play"

                if self.pause_button_rect.collidepoint(event.pos[0] - self.Cons.ARENA_WIDTH, event.pos[1]) and self.pause_button_enable:
                    print("Pause button clicked")
                    self.pause_button_enable = False
                    self.play_button_enable = True
                    return "Pause"

                if self.reset_button_rect.collidepoint(event.pos[0] - self.Cons.ARENA_WIDTH, event.pos[1]):
                    print("Reset button clicked")
                    return "Reset"



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    def quit(self):
        pygame.quit()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to add text to surface on position
    def add_text(self, surface, font, text, position):
        text_surface = font.render(text, True, self.RGB_COLORS.black)
        surface.blit(text_surface, position)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # Function to add a progress bar to the surface
    def add_progress_bar(self, surface, position, width, height, value, max_value, color):
        # Draw the progress bar background
        pygame.draw.rect(surface, self.RGB_COLORS.light_gray, (position[0], position[1], width, height))

        # Draw the progress bar fill
        fill_width = (value / max_value) * width
        pygame.draw.rect(surface, color, (position[0], position[1], fill_width, height))

        # Draw the progress bar border
        border_color = self.RGB_COLORS.black
        border_width = 1
        pygame.draw.rect(surface, border_color, (position[0], position[1], width, height), border_width)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    def add_button(self, surface, button_rect, button_color, text, text_font, is_enabled):

        # Draw the button rectangle border
        border_width = 1
        border_color = self.RGB_COLORS.black
        border_rect = pygame.Rect(button_rect.left - border_width, button_rect.top - border_width, button_rect.width + 2*border_width, button_rect.height + 2*border_width)
        pygame.draw.rect(surface, border_color, border_rect)
        
        # Draw the button rectangle color based on its enabled state
        if is_enabled:
            pygame.draw.rect(surface, button_color, button_rect)
        else:
            pygame.draw.rect(surface, self.RGB_COLORS.light_gray, button_rect)

        # Render and blit the button text
        text_render = text_font.render(text, True, self.RGB_COLORS.black)
        text_rect = text_render.get_rect(center=button_rect.center)
        surface.blit(text_render, text_rect)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #


# Class Colors
class RGB_COLORS:
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 200, 0)
    blue = (0, 0, 255)
    orange = (255, 165, 0)
    red = (255, 0, 0)
    yellow = (255, 255, 0)
    cornflower_blue = (51, 179, 232)
    light_gray = (192, 192, 192)
    gray = (128, 128, 128)
    Turquoise = (64, 224, 208)
    purple = (128, 0, 128)
    magenta = (255, 0, 255)
    cyan = (0, 255, 255)
    olive = (128, 128, 0)



