# Metadata
#=========
__author__ = "Luis Domingues"
__maintainer__ = "Luis Domingues"
__email__ = "luis.hmd@gmail.com"

#----------------------------------------------------------------------------------------
# Notes
#----------------------------------------------------------------------------------------
# This could be converted into one function in lib_sports called count_week_totals

#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
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
    # Print week activities
    lib_print.print_week_activities_names(activities_dir, week)