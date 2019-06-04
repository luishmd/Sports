__author__ = 'luisd'

#----------------------------------------------------------------------------------------
# Notes
#----------------------------------------------------------------------------------------
# This could be converted into one function in lib_sports called count_week_totals

#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
import lib_sport_ops as lib_sports
import lib_directory_ops as lib_dir
import lib_sport_printing as lib_print

#----------------------------------------------------------------------------------------
# INPUTS
#----------------------------------------------------------------------------------------
username = lib_dir.getpass.getuser()
root_dir = "C:/Users/" + username + "/Google Drive/Treinos/Activities/"

week = "W47 - 20 Aug - 26 Aug/"

#----------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------
[total_time, total_distance, total_calories, heart_rate_profile, speed_profile, cadence_profile, latitude_profile, longitude_profile, altitude_profile, distance_profile] = lib_sports.get_data_week_activities(root_dir, week)

# Printing results
lib_print.print_total_time(total_time)
#lib_print.print_total_distance(total_distance)