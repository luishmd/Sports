# Metadata
#=========
__author__ = "Luis Domingues"
__maintainer__ = "Luis Domingues"
__email__ = "luis.hmd@gmail.com"


#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
import lib_sport_ops as lib_sports
import lib_sport_printing as lib_print
import lib_path_ops
import yaml
import sys
import os

#----------------------------------------------------------------------------------------
    # PRE-CALCULATIONS
#----------------------------------------------------------------------------------------
# Get inputs
root_dir = os.getcwd()
root_dir = root_dir+'/'

#----------------------------------------------------------------------------------------
# INPUTS
#----------------------------------------------------------------------------------------
try:
    input_file = lib_path_ops.join_paths(root_dir, 'inputs/inputs.yaml')
    with open(input_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    activities_dir = cfg['activities path']
    week = cfg['week']
    print("Loaded inputs successfully.")
except:
    print("Failed to load inputs. Exiting...")
    sys.exit(1)

#----------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    [total_time, total_distance, total_calories, heart_rate_profile, speed_profile, cadence_profile, latitude_profile, longitude_profile, altitude_profile, distance_profile] = lib_sports.get_data_week_activities(activities_dir, week)

    # Printing results
    lib_print.print_total_time(total_time)
    #lib_print.print_total_distance(total_distance)