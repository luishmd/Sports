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
root_dir = "C:/Users/" + username + "/Google Drive/Treinos/2016_17/Activities/"

week = "W32 - 7 Aug - 13 Aug/"
activity_name = "Running on 12 August 2017 at 08:06:47"

# link to database/excel
heart_rate_dic = {"Z1":[84,142],
                  "Z2":[143,152],
                  "Z3":[153,159],
                  "Z4":[160,167],
                  "Z5":[168,184]}

delta_from_end_min=10;

#----------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------
# Print week activities
#lib_print.print_week_activities_names(root_dir, week)

# Get path to file
week_activities_names_paths = lib_sports.get_dic_week_activities_names_paths(root_dir, week)
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


