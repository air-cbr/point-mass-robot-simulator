"""
Simulation class

This class handles the "Point Mass Robot simulation"
The class is responsible for the simulation loop to control robot movement, communication, and performance metrics, and GUI.
The class also handles the "Boids Algorithm" for the coverage task.


@ Author            Reda Ghanem
@ Version           1.0
@ Last update       11/11/2023
"""


# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ********************  importing libraries and classes  ************************ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #


# [1]- importing libraries
import time                         # for time measurements
import sys, os                      # to obtain the current path and Set working directory to current_directory
import random                       # for random number generation
random.seed(30)                     # Set the seed for random number generation to ensure reproducibility

# [2]- very important if you want to access all files and Modules from current_directory
# Get the current directory and append it to the system path
current_directory, filename = os.path.split(os.path.abspath(__file__))  # Get the current directory of the current file
sys.path.append(current_directory)                                      # Append the current directory to the system path

# [3]- importing Classes and Functions
from Boids_Assets.Constants import Constants                            # for Constants and Global variables
from Evaluation_Assets.Performance_Metrics import Performance_Metrics   # for Performance Metrics
from Robot import Robot                                                 # for Robot class
from Boids_Assets.Helper_Functions import *                             # for helper functions ex. normalize_speed_limit ...




# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #


# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
# ┃------------------------ # Simulation Class # ------------------------------┃ #
# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #

class Simulation:

    def __init__(self, tunable_parameters = None, print_tunable_parameters_status = True, GUI = True):

        self.tunable_parameters = tunable_parameters    # receive tunable parameters from main code. so we can use it when we reset the simulation
        self.Cons = Constants(tunable_parameters, print_tunable_parameters_status, GUI)       # Constants and Global variables

        # initializations
        self.Performance_Metrics = Performance_Metrics(self.Cons)
        self.running             = True
        self.time_step           = 0
        self.start_robot_heading_angle = 0             # heading_angle in radian, 1.57079 means looks in +Y direction, -1.57079 means looks in -Y direction, 0 means looks in +X direction


        # Show GUI if Cons.RENDERING is True
        if self.Cons.RENDERING == True:
            # use import Environment here to avoid : Hello from the pygame community
            from GUI_Assets.Environment import Environment
            # clear the console to avoid message: Hello from the pygame community
            clear_console()
            # initialize Environment, send Cons and Performance_Metrics to Environment to use it in GUI
            self.environment = Environment(self.Cons, self.Performance_Metrics)

        # initialize Robots
        self.robots = []        # To hold all Robots objects
        self.boids = []         # To hold all Boids objects
        for index in range(0, self.Cons.NUM_OF_ROBOTS):
            start_pos = self.Cons.ROBOTS_POSITIONS[index]     # get start position for this robot

            if self.Cons.RENDERING == True:
                skin = random.choice(list(self.environment.ROBOT_SKINS.values()))       # pick a random skin for this robot
            else:
                skin = None

            robot = Robot(self.Cons, start_pos, self.start_robot_heading_angle, self.Cons.ROBOT_SIZE, skin, index)
            self.robots.append(robot)

            # get reference for this boids to use it in simulation and Performance_Metrics
            self.boids.append(robot.boid)


        random.seed(30)         # Set the seed for random number generation to ensure reproducibility

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # function to run the simulation
    def run(self):

        # Step[01]: in case we use GUI, start with "Pause"
        if self.Cons.RENDERING == True:
            self.environment.draw_window(self.robots, self.boids)     # Show GUI screen window
            self.running = "Pause"

        # Step[02]: start real time for the experemint
        start_time = time.time()  # Get the current time

        # -------------------------------------------------------------------------------- #
        # ---------------------------- Start of Simulation Loop -------------------------- #
        # -------------------------------------------------------------------------------- #
        # Step[03]: Start the Simulation and Animation loop
        while self.running != False:

            # Step[3.1]: First Step Check if self.Cons.RENDERING is True, Then check user event
            if self.Cons.RENDERING == True:
                event = self.environment.check_event()          # get current user event

                if  event == "QUIT":
                    # Terminate the Simulation
                    self.running = False
                    break

                elif event == "Play":
                    # Resume the Simulation
                    self.running = True
                    # ignore time of "Pause", so we only have real time of running
                    start_time = time.time() - self.Performance_Metrics.EXPERIMENT_RUNTIME

                elif event == "Pause":
                    # Pause the Simulation
                    self.running = "Pause"

                elif event == "Reset":
                    # Reset the Simulation
                    self.running = "Reset"
                    self.__init__(self.tunable_parameters)
                    self.run()
                    self.running = False
                    break

                if self.running == "Pause":
                    self.environment.draw_window(self.robots, self.boids)       # Draw last GUI frame
                    continue


            # Step[3.2]: For optimization, check if coverage task is completed or not
            # Check if TT > MAX_STOP_TIME or all GLOBAL_UFCO_MATRIX cells explored (2 or 3)
            if self.Performance_Metrics.check_task_completed() == True:
                if self.Cons.RENDERING == True:
                    self.running = "Pause"
                    self.environment.play_button_enable = False
                    self.environment.pause_button_enable = False
                    continue
                else:
                    self.running = False
                    break


            # Step[3.3]: For each (Robot) update_ufco_matrix_coverage from the current cell
            for robot in self.robots:
                robot.boid.update_ufco_matrix_coverage()

            # Step [3.4]: For each (Robot) send_information to server_data
            # we skip this step and we will use robots list in function receive_information
            # for robot in robots:
            #     server_data += robot.send_information()

            # Step [3.5]: For each (Robot) receive_information
            for robot in self.robots:
                robot.receive_information(self.robots)

            # Step [3.6]: For each (Robot) Update boid ufco_matrix from shared neighbors_ufco_matrices of neighbors which in range of SHARE_RANGE
            for robot in self.robots:
                robot.boid.share_ufco_matrix(robot.boid.neighbors_positions, robot.boid.neighbors_ufco_matrices)

            # Step [3.7]: For each (Robot) compute the next step by update_velocity before moving any robot
            for robot in self.robots:
                robot.boid.update_velocity()

            # Step [3.8]: For each (Robot) moving now by updating position and heading angle
            for robot in self.robots:
                robot.boid.update_position()
                robot.boid.update_heading_angle()

            # Step [3.9]: Update current time and time_step
            current_time = time.time()                  # time.time(): Get the current time
            self.time_step += 1

            # Step [3.10]: Update Performance Metrics
            self.Performance_Metrics.updat_performance_metrics(self.boids, start_time, current_time, self.time_step)

            # Step [3.11]: Draw the graphical user interface (GUI)
            if self.Cons.RENDERING == True:
                # To control the speed of drawing simulation
                if self.time_step % self.Cons.SPEED_OF_SIMULATION == 0:
                    # Show GUI screen window
                    self.environment.draw_window(self.robots, self.boids)

        # -------------------------------------------------------------------------------- #
        # ---------------------------- End of Simulation Loop ---------------------------- #
        # -------------------------------------------------------------------------------- #

        # Step [04]: Terminate the simulation GUI
        if self.Cons.RENDERING == True:
            self.environment.quit()

        # Step [05]: return results (V, CP, DC, TT)
        return self.Performance_Metrics.VIOLATIONS, self.Performance_Metrics.COVERAGE_PERCENTAGE, self.Performance_Metrics.TURNAROUND_TIME

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    # function to print Performance Metrics
    def print_resuts(self):

        # Print Results
        print(f"\n{'=' * 9} # {'Experiment Results'} # {'=' * 9}")
        print("Experiment Runtime  =" , f"{self.Performance_Metrics.EXPERIMENT_RUNTIME:.2f} Seconds")
        print("Coverage Count      =" , f"{self.Performance_Metrics.COVERAGE_COUNT}/{self.Cons.TOTAL_CELLS}" )

        # Print Performance Metrics
        print(f"\n{'=' * 9} # {'Performance Metrics'} # {'=' * 9}")
        print("Violations          =" , f"{self.Performance_Metrics.VIOLATIONS}" )
        print("Coverage Percentage =" , f"{self.Performance_Metrics.COVERAGE_PERCENTAGE:.2f}%" )
        print("Turnaround Time     =" , f"{self.Performance_Metrics.TURNAROUND_TIME:.2f} Seconds")     # Print the time taken by robots to cover the environment
        # print("GLOBAL_UFCO_MATRIX  =")

      

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#               ███╗░░░███╗░█████╗░██╗███╗░░██╗               #
#               ████╗░████║██╔══██╗██║████╗░██║               #
#               ██╔████╔██║███████║██║██╔██╗██║               #
#               ██║╚██╔╝██║██╔══██║██║██║╚████║               #
#               ██║░╚═╝░██║██║░░██║██║██║░╚███║               #
#               ╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝╚═╝░░╚══╝               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Function to convert last 6 value in parameters from meter to cm
def convert_ranges_to_cm(parameters):

    for i in range (0,len(parameters)):
        if i >= 6:
            parameters[i] = parameters[i] * 100

    return parameters
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# test case
def main():

    # use tunable_parameters = None # if you want to use tunable_parameters from Configuration.json file
    tunable_parameters = None

    # From optimization with DC using point mass simulator
    tunable_parameters = [0.36164, 0.95762, 0.78499, 0.97822, 0.10081, 0.78677, 286, 41, 65, 67, 51, 280]


    simulation = Simulation(tunable_parameters, True, True)

    # Run the simulation in the main thread
    simulation.run()

    # print Performance Metrics
    simulation.print_resuts()

    # Terminate the programe
    sys.exit()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #

if __name__ == '__main__':

    main()


    
