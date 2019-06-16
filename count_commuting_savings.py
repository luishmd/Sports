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
    journey_price = cfg['journey_price']
    travelcard_cap = cfg['travelcard_cap']
    print("Loaded inputs successfully.")
except:
    print("Failed to load inputs. Exiting...")
    sys.exit(1)

#----------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------
weeks_names = lib_sports.get_names_weeks(activities_dir)
week_savings_dic = {}
total_savings = 0
for week in weeks_names:
    week_savings_dic[week] = lib_sports.calc_savings_week_commute(activities_dir, week+"/", journey_price=journey_price, travelcard_cap=travelcard_cap)
    total_savings += week_savings_dic[week]

# Print results
lib_print.print_commuting_savings(week_savings_dic, total_savings)