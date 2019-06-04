# Metadata
#=========
__author__ = 'Luis Domingues'

# Description
#============
# Library that provides xml operations

# Notes
#======
#

# Known issues/enhancements
#==========================
#

#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
import lib_sport_ops as lib_sports
import math as lib_math
import lib_datetime_ops as lib_datetime


#----------------------------------------------------------------------------------------
# FUNCTIONS
#----------------------------------------------------------------------------------------
def print_time_in_hr_zones(hr_time_profile):
    """
    Function that prints the amount of time spent in each heart rate zone
    """
    if hr_time_profile:
        print("\nTIME IN HR ZONES\n")
        for key in hr_time_profile.keys():
            print(key + ": " + str(hr_time_profile[key]))
    return 0


def print_week_activities(week_activities_dic):
    """
    Function that prints all the names of the activities in a given week
    """
    week_activities_names = lib_sports.get_names_week_activities(week_activities_dic)
    for week_activity_name in week_activities_names:
        print(week_activity_name)
    return 0


def print_total_time(total_time_seconds):
    """
    Function that prints the total time spent in each activity
    """
    print("\nTOTAL TIME\n")
    for sport_type in total_time_seconds.keys():
        print("%s\t%.2f" %(sport_type, total_time_seconds[sport_type]/60.0))
    return 0


def print_total_distance(total_distance):
    """
    Function that prints the total distance of each activity
    """
    print("\nTOTAL DISTACE\n")
    for sport_type in total_distance.keys():
        print("%s\t%.1f" %(sport_type, total_distance[sport_type]/1000.0))
    return 0

def print_commuting_savings(week_savings_dic, total_savings):
    """
    Function that prints the commuting savings by week and the total savings
    """
    print("\nSAVINGS\n")
    for week in sorted(week_savings_dic.keys()):
        print("%s: %.2f GBP" % (week, week_savings_dic[week]))
    print("\n")
    print("Total money saved = %.2f GBP" % total_savings)
    return 0


def print_week_activities_names(root_dir, week):
    week_activities_names_lst = lib_sports.get_names_week_activities(root_dir, week)
    if week_activities_names_lst:
        print("\nWEEK ACTIVITIES\n")
        for activity in week_activities_names_lst:
            print(activity)
    return 0


def print_activity_averages(average_hr, average_speed, average_cadence, additional="", run=True, cycle=False):
    print("\nAVERAGES " + additional + "\n")
    print("Heart rate: %.0f bpm" %round(average_hr))
    print("Speed: %.2f km/h" % lib_sports.convert_speed_to_km_per_h(average_speed))
    print("Pace: %s" % print_pace(lib_sports.convert_speed_to_pace(average_speed)))
    if run:
        print("Cadence: %.0f spm" % round(2.0*average_cadence))
    if cycle:
        print("Cadence: %.0f spm" % round(average_cadence))
    return 0


def print_activity_totals(total_time_seconds, total_distance, total_calories):
    """
    Function that prints the total time spent in the activity
    """
    print("Total time: %s" %print_time(total_time_seconds))
    print("Total distance: %.1f km" %(total_distance/1000))
    print("Total calories: %i cal" %total_calories)
    return 0


def print_pace(pace_min_km):
    """
    Function that prints the pace in min/km
    """
    min = lib_math.floor(pace_min_km)
    sec = lib_math.floor((pace_min_km - min)*60.0)
    if lib_math.floor(sec/10) >= 1:
        pace = "%i:%i min/km" %(int(min), int(sec))
    else:
        pace = "%i:0%i min/km" % (int(min), int(sec))
    return pace


def print_time(time_seconds):
    """
    Function that prints the time
    """
    time_str = lib_datetime.create_timedelta_object(time_seconds)
    return time_str

#----------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass