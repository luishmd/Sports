__author__ = 'luisd'

#----------------------------------------------------------------------------------------
# Notes
#----------------------------------------------------------------------------------------
# Script used for validation of the extract activity data. This is an auxiliary script without further use

#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
import lib_sport_ops as lib_sports
import lib_directory_ops as lib_dir
import lib_file_ops as lib_file
import lib_sport_printing as lib_print

#----------------------------------------------------------------------------------------
# INPUTS
#----------------------------------------------------------------------------------------
username = lib_dir.getpass.getuser()
root_dir = "C:/Users/" + username + "/Google Drive/Treinos/Activities/"

file_path = "C:/Users/" + username + "/Documents/Programming/SVN_coding_repo/trunk/training/scripts/_auxilary_files_not_tracked/output.txt"

week = "W13 - 27 Mar - 2 Apr/"
activity_name = "Running on 01 April 2017 at 09:11:22"

# link to database/excel
heart_rate_dic = {"Z1":[0,131],
                  "Z2":[132,147],
                  "Z3":[148,155],
                  "Z4":[156,166],
                  "Z5":[167,5000]}

delta_from_end_min=20;

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

f = lib_file.open_file(file_path, "w+")


print len(speed_profile_laps[1][0])

print "%i\t%1.10f" % (0, speed_profile_laps[1][1][0])
for i in range(1,len(speed_profile_laps[1][0])-1):
    delta = speed_profile_laps[1][0][i] - speed_profile_laps[1][0][i - 1]
    print "%1.1f\t%1.10f" %(delta.total_seconds(), speed_profile_laps[1][1][i])

lib_file.write_to_file(f, "Hello")

lib_file.close_file(f)