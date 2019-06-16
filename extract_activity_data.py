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
    activity_name = cfg['activity_name']
    heart_rate_dic = cfg['heart_rate_dic']
    delta_from_end_min = cfg['delta_from_end_min']
    print("Loaded inputs successfully.")
except:
    print("Failed to load inputs. Exiting...")
    sys.exit(1)



#----------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Print week activities
    #lib_print.print_week_activities_names(root_dir, week)

    # Get path to file
    week_activities_names_paths = lib_sports.get_dic_week_activities_names_paths(activities_dir, week)
    activity_name_path = week_activities_names_paths[activity_name]

    # Extract profiles
    [activity_datetime, total_time, total_distance, total_calories, heart_rate_profile_act, speed_profile_act, cadence_profile, latitude_profile, longitude_profile, altitude_profile, distance_profile] = lib_sports.get_data_activity(activity_name_path)
    [total_time_laps, total_distance_laps, total_calories_laps, heart_rate_profile_laps, speed_profile_laps, cadence_profile_laps, latitude_profile_laps, longitude_profile_laps, altitude_profile_laps, distance_profile_laps] = lib_sports.get_data_activity_laps(activity_name_path)

    # Print totals
    lib_print.print_activity_totals(total_time, total_distance, total_calories)

    # Get time in HR zones
    time_in_hr_zones = lib_sports.calc_time_in_heart_rate_zones_activity(heart_rate_profile_act, heart_rate_dic)
    lib_print.print_time_in_hr_zones(time_in_hr_zones)

    # Get averages - total
    [average_hr, average_speed, average_cadence] = lib_sports.calc_average_data(heart_rate_profile_act, speed_profile_act, cadence_profile)
    add_descriptor = "(total)"
    lib_print.print_activity_averages(average_hr, average_speed, average_cadence, add_descriptor)

    # Get averages - laps
    for lap in total_time_laps.keys():
        [average_hr, average_speed, average_cadence] = lib_sports.calc_average_data(heart_rate_profile_laps[lap], speed_profile_laps[lap], cadence_profile_laps[lap])
        add_descriptor = "(lap %i)" %lap
        lib_print.print_activity_averages(average_hr, average_speed, average_cadence, add_descriptor)

    # Get averages - partial
    [average_hr, average_speed, average_cadence] = lib_sports.calc_average_data(heart_rate_profile_act, speed_profile_act, cadence_profile, timedelta_from_end_min=delta_from_end_min)
    add_descriptor = "(last %i min)" %delta_from_end_min
    lib_print.print_activity_averages(average_hr, average_speed, average_cadence, add_descriptor)


