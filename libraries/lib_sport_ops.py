# Metadata
#=========
__author__ = "Luis Domingues"
__maintainer__ = "Luis Domingues"
__email__ = "luis.hmd@gmail.com"

# Description
#============
# Library that provides sport-related operations


#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
import lib_file_ops as lib_file
import lib_directory_ops as lib_dir
import lib_sport_xml_ops as lib_xml
import lib_datetime_ops as lib_datetime
import lib_sport_formatting as lib_format
import lib_general_ops as lib_general
import conversion_lib as lib_conv


#----------------------------------------------------------------------------------------
# FUNCTIONS
#----------------------------------------------------------------------------------------
def get_dic_week_activities(root_dir, week):
    """
    Function that builds the dictionary for week activities and returns it.
        sports_types - list containing all the possible sports types (e.g. Running, cycling). These are the directory names.
        week_path - string containing the path to the folder containing the activities
        sport_activities - list containing the full path for each activity of a given type
    """
    week_activities_dic = {}
    week_path = root_dir + week
    sports_types = get_sports_types(root_dir, week)
    for sport_type in sports_types:
        path = week_path + sport_type + "/"
        sport_activities = lib_file.get_files_complete_names_with_extensions(path)
        week_activities_dic[str(sport_type)] = sport_activities
    return week_activities_dic


def get_dic_week_activities_names_paths(root_dir, week):
    """
    Function that creates a dictionary where the keys are the activities names and the value is the path to the activity file
     activity name -> Running on 06 March 2017 at 19:22:03
     value -> C:/Users/luisd/Google Drive/Treinos/Activities/W14 - 3 Apr - 9 Apr/Running/activity_1660306289.tcx
    """
    week_activities_names_paths = {}
    week_path = root_dir + week
    sports_types = get_sports_types(root_dir, week)
    for sport_type in sports_types:
        path = week_path + sport_type + "/"
        sport_activities = lib_file.get_files_complete_names_with_extensions(path)
        for sport_activity in sport_activities:
            start_datetime_obj = get_activity_start_datetime(sport_activity)
            week_activities_names_paths[lib_format.format_name_activity(sport_type, start_datetime_obj)] = sport_activity
    return week_activities_names_paths


def get_sports_types(root_dir, week):
    """
    Function that returns the sports types (correspond to the directory names for a given week)
    """
    week_path = root_dir + week
    sports_types = lib_dir.listdir(week_path)
    return sports_types


def get_names_weeks(root_dir):
    """
    Function that returns all the week names as a list
    """
    weeks_names = lib_dir.listdir(root_dir)
    try:
        weeks_names.remove("WX- dd mmm - dd mmm")
    except:
        pass
    return weeks_names


def get_names_week_activities(root_dir, week):
    """
    Function that returns the week activities names as a list
    """
    activities_names = []
    week_activities_dic = get_dic_week_activities(root_dir, week)
    for sport_type in week_activities_dic.keys():
        for activity in week_activities_dic[sport_type]:
            datetime_obj = get_activity_start_datetime(activity)
            activities_names.append(lib_format.format_name_activity(sport_type, datetime_obj))
    return activities_names


def get_names_all_activities(root_dir):
    """
    Function that returns all activities names as a list
    """
    activities_names = []
    weeks_names = get_names_weeks(root_dir)
    for week_name in weeks_names:
        week_activities_names = get_dic_week_activities(root_dir, week_name)
        for week_activities_name in week_activities_names:
            activities_names.append(week_activities_name)
    return activities_names


def get_activity_start_datetime(activity_path):
    """
    Function that returns the start time of an activity as a datetime object
    activity_path -> C:/Users/luisd/Google Drive/Treinos/Activities/W14 - 3 Apr - 9 Apr/Running/activity_1660306289.tcx
    """
    [tree, root] = lib_xml.parse_tree(activity_path)
    start_datetime_obj = lib_xml.extract_activity_datetime(root)
    return start_datetime_obj


def get_data_week_activities(root_dir, week):
    """
    Function that builds the dictionary for week activities and returns it.
        sports_types - list containing all the possible sports types (e.g. Running, cycling). These are the directory names.
        week_path - string containing the path to the folder containing the activities
    """
    # Define dictionaries
    total_time_week_dic = {}
    total_distance_week_dic = {}
    total_calories_week_dic = {}
    heart_rate_profile_week_dic = {}
    speed_profile_week_dic = {}
    cadence_profile_week_dic = {}
    latitude_profile_week_dic = {}
    longitude_profile_week_dic = {}
    altitude_profile_week_dic = {}
    distance_profile_week_dic = {}
    # Get week activities dictionary
    week_activities_dic = get_dic_week_activities(root_dir, week)
    # Extract info from each activity
    for sport_type in week_activities_dic.keys():
        total_time_week_dic[sport_type] = 0
        total_distance_week_dic[sport_type] = 0
        for activity in week_activities_dic[sport_type]:
            [activity_datetime, total_time, total_distance, total_calories, heart_rate_profile, speed_profile, cadence_profile, latitude_profile,longitude_profile, altitude_profile, distance_profile] = get_data_activity(activity)
            # Add to dictionaries
            total_time_week_dic[sport_type] += total_time
            total_distance_week_dic[sport_type] += total_distance # Only when gps is tracking. If added later, then TCX does not contain it.
            # Heart rate
            heart_rate_profile_week_dic[lib_format.format_name_activity(sport_type, activity_datetime)] = heart_rate_profile
            # Speed
            speed_profile_week_dic[lib_format.format_name_activity(sport_type, activity_datetime)] = speed_profile
            # Cadence
            cadence_profile_week_dic[lib_format.format_name_activity(sport_type, activity_datetime)] = cadence_profile
            # Position
            latitude_profile_week_dic[lib_format.format_name_activity(sport_type, activity_datetime)] = latitude_profile
            longitude_profile_week_dic[lib_format.format_name_activity(sport_type, activity_datetime)] = longitude_profile
            # Altitude
            altitude_profile_week_dic[lib_format.format_name_activity(sport_type, activity_datetime)] = altitude_profile
            # Distance
            distance_profile_week_dic[lib_format.format_name_activity(sport_type, activity_datetime)] = distance_profile
    return [total_time_week_dic, total_distance_week_dic, total_calories_week_dic, heart_rate_profile_week_dic, speed_profile_week_dic, cadence_profile_week_dic, latitude_profile_week_dic, longitude_profile_week_dic, altitude_profile_week_dic, distance_profile_week_dic]


def get_data_activity(activity_name_path):
    """
    Function that returns the profiles of a given activity
    activity_name_path -> C:/Users/luisd/Google Drive/Treinos/Activities/W10 - 6 Mar - 12 Mar/Swimming/
    """
    # Parse tree
    [tree, root] = lib_xml.parse_tree(activity_name_path)
    # Extract activity date and time of day
    activity_datetime = lib_xml.extract_activity_datetime(root)
    # Extract time profiles
    [time, heart_rate, speed, cadence, latitude, longitude, altitude, distance] = lib_xml.extract_activity_time_profiles(root)
    # Get activity totals
    [total_time, total_distance, total_calories] = lib_xml.extract_activity_totals(root)
    # Get activity heart rate
    heart_rate_profile = [time, heart_rate]
    # Get activity speed
    speed_profile = [time, speed]
    # Get activity cadence
    cadence_profile = [time, cadence]
    # Get activity position
    latitude_profile = [time, latitude]
    longitude_profile = [time, longitude]
    # Get activity altitude
    altitude_profile = [time, altitude]
    # Get activity distance
    distance_profile = [time, distance]
    return [activity_datetime, total_time, total_distance, total_calories, heart_rate_profile, speed_profile, cadence_profile, latitude_profile, longitude_profile, altitude_profile, distance_profile]


def get_data_activity_laps(activity_name_path):
    """
    Function that returns the lap profiles of a given activity
    activity_name_path -> C:/Users/luisd/Google Drive/Treinos/Activities/W10 - 6 Mar - 12 Mar/Swimming/
    """
    # Define dictionaries
    total_time_lap_dic = {}
    total_distance_lap_dic = {}
    total_calories_lap_dic = {}
    heart_rate_profile_lap_dic = {}
    speed_profile_lap_dic = {}
    cadence_profile_lap_dic = {}
    latitude_profile_lap_dic = {}
    longitude_profile_lap_dic = {}
    altitude_profile_lap_dic = {}
    distance_profile_lap_dic = {}
    # Parse tree
    [tree, root] = lib_xml.parse_tree(activity_name_path)
    # Get lap elements
    laps_element_list = lib_xml.extract_activity_laps(root)
    # get the data
    lap = 1
    for lap_element in laps_element_list:
        [total_lap_time, total_lap_distance, total_lap_calories] = lib_xml.extract_lap_totals_trackpoint_based(lap_element)
        [time, heart_rate, speed, cadence, latitude, longitude, altitude, distance] = lib_xml.extract_lap_time_profiles(lap_element)
        # Get activity lap data
        total_time_lap_dic[lap] = total_lap_time
        total_distance_lap_dic[lap] = total_lap_distance  # Only when gps is tracking. If added later, then TCX does not contain it.
        total_calories_lap_dic[lap] = total_lap_calories
        # Get activity lap heart rate
        heart_rate_profile_lap_dic[lap] = [time, heart_rate]
        # Get activity lap speed
        speed_profile_lap_dic[lap] = [time, speed]
        # Get activity lap cadence
        cadence_profile_lap_dic[lap] = [time, cadence]
        # Get activity lap position
        latitude_profile_lap_dic[lap] = [time, latitude]
        longitude_profile_lap_dic[lap] = [time, longitude]
        # Get activity lap altitude
        altitude_profile_lap_dic[lap] = [time, altitude]
        # Get activity lap distance
        distance_profile_lap_dic[lap] = [time, distance]
        # Increment lap
        lap = lap + 1
    return [total_time_lap_dic, total_distance_lap_dic, total_calories_lap_dic, heart_rate_profile_lap_dic, speed_profile_lap_dic, cadence_profile_lap_dic, latitude_profile_lap_dic, longitude_profile_lap_dic, altitude_profile_lap_dic, distance_profile_lap_dic]


def calc_savings_week_commute(root_dir, week, journey_price_GBP=1.5, travelcard_cap=4.5):
    """
    Function that calculates the savings for commuting on a bike during a week
    """
    total_savings = 0
    commute_counter_dic = {}
    commute_savings_dic = {}
    week_activities_dic = get_dic_week_activities(root_dir, week)
    week_commutes = week_activities_dic["Commuting"]
    # Get dictionaries with number of commutes per day in a week
    for commute in week_commutes:
        datetime_obj = get_activity_start_datetime(commute)
        date = lib_datetime.format_date(datetime_obj)
        if date in commute_counter_dic:
            commute_counter_dic[date] += 1
        else:
            commute_counter_dic[date] = 1
    # Calculate savings
    dates = commute_counter_dic.keys()
    for date in dates:
        commute_savings_dic[date] = commute_counter_dic[date]*journey_price_GBP
        if commute_savings_dic[date] > travelcard_cap:
            commute_savings_dic[date] = travelcard_cap
        total_savings += commute_savings_dic[date]
    return total_savings


def calc_average_data(heart_rate_profile=[], speed_profile=[], cadence_profile=[], datetime_start=0, datetime_end=0, timedelta_from_start=0, timedelta_from_end=0, timedelta_from_start_min=0, timedelta_from_end_min=0):
    """
    Function that calculates the average data (heart rate, speed, cadence, etc) for a given period of an activity
    Can specify:
        - Nothing - calculates average for entire profiles
        - Time start and time end calculates averages across a time region
        - delta from beginning - calculates averages from begining to beg + delta
        - delta from end - same but uses end instead of beg
    """
    average_hr = 0.0
    average_speed = 0.0
    average_cadence = 0.0
    if timedelta_from_start_min:
        timedelta_from_start = lib_datetime.create_timedelta_object(timedelta_from_start_min*60)
    if timedelta_from_end_min:
        timedelta_from_end = lib_datetime.create_timedelta_object(timedelta_from_end_min*60)
    if heart_rate_profile[0]:
        sum_hr = 0.0
        [start_idx, end_idx] = get_start_and_end_indexes(heart_rate_profile[0], datetime_start, datetime_end, timedelta_from_start, timedelta_from_end)
        duration = heart_rate_profile[0][end_idx] - heart_rate_profile[0][start_idx]
        for i in range(start_idx, end_idx):
            delta = heart_rate_profile[0][i+1] - heart_rate_profile[0][i]
            average_hr_aux = (heart_rate_profile[1][i+1] + heart_rate_profile[1][i]) / 2
            sum_hr = sum_hr + average_hr_aux * delta.total_seconds()
        average_hr = sum_hr / duration.total_seconds()
    if speed_profile[0]:
        sum_speed = 0.0
        [start_idx, end_idx] = get_start_and_end_indexes(speed_profile[0], datetime_start, datetime_end, timedelta_from_start, timedelta_from_end)
        duration = speed_profile[0][end_idx] - speed_profile[0][start_idx]
        for i in range(start_idx, end_idx):
            delta = speed_profile[0][i + 1] - speed_profile[0][i]
            average_speed_aux = (speed_profile[1][i + 1] + speed_profile[1][i]) / 2
            sum_speed = sum_speed + average_speed_aux * delta.total_seconds()
        average_speed = sum_speed / duration.total_seconds()
    if cadence_profile[0]:
        sum_cadence = 0.0
        [start_idx, end_idx] = get_start_and_end_indexes(cadence_profile[0], datetime_start, datetime_end, timedelta_from_start, timedelta_from_end)
        duration = cadence_profile[0][end_idx] - cadence_profile[0][start_idx]
        for i in range(start_idx, end_idx):
            delta = cadence_profile[0][i + 1] - cadence_profile[0][i]
            average_cadence_aux = (cadence_profile[1][i + 1] + cadence_profile[1][i]) / 2
            sum_cadence = sum_cadence + average_cadence_aux * delta.total_seconds()
        average_cadence = sum_cadence / duration.total_seconds()
    return [average_hr, average_speed, average_cadence]


def get_start_and_end_indexes(time_profile, datetime_start, datetime_end, timedelta_from_start, timedelta_from_end):
    """
    Function that determines the start and end indexes of the time profile to determine averages.
    """
    start_idx = 0
    end_idx = len(time_profile) - 1
    if datetime_start == 0 and datetime_end == 0 and timedelta_from_start == 0 and timedelta_from_end == 0:
        return [start_idx, end_idx]
    else:
        if datetime_start:
            start_idx = lib_general.get_index_in_list(time_profile, datetime_start)
        if datetime_end:
            end_idx = lib_general.get_index_in_list(time_profile, datetime_end)
        if timedelta_from_start:
            datetime_start = time_profile[0]
            start_idx = lib_general.get_index_in_list(time_profile, datetime_start + timedelta_from_start)
        if timedelta_from_end:
            datetime_end = time_profile[len(time_profile) - 1]
            start_idx = lib_general.get_index_in_list(time_profile, datetime_end - timedelta_from_end)
        return [start_idx, end_idx]


def calc_time_in_heart_rate_zones_activity(heart_rate_profile, heart_rate_zones_dic):
    """
    Function that calculates the time spent in a given heart rate zone of an activity
    """
    time_in_zones = {}
    hr_zones = heart_rate_zones_dic.keys()
    # Initialise dictionary
    for hr_zone in hr_zones:
        time_in_zones[hr_zone] = lib_datetime.timedelta(0)
    if heart_rate_profile[0]:
        # Only if list is not empty
        # 1st argument is list of datertime objects; second argument is list of heart rates
        datetime_start = heart_rate_profile[0][0]
        hr_start = heart_rate_profile[1][0]
        # Go through the list
        for i in range(len(heart_rate_profile[0])-1):
            datetime_end = heart_rate_profile[0][i+1]
            hr_end = heart_rate_profile[1][i+1]
            hr_zone_start = get_heart_rate_zone(heart_rate_zones_dic, hr_start)
            hr_zone_end = get_heart_rate_zone(heart_rate_zones_dic, hr_end)
            delta = datetime_end - datetime_start
            if test_change_heart_rate_zone(heart_rate_zones_dic, hr_start, hr_end):
                time_in_zones[hr_zone_start] = time_in_zones[hr_zone_start] + delta/2
                time_in_zones[hr_zone_end] = time_in_zones[hr_zone_end] + delta / 2
            else: # start and end are in the same zone
                time_in_zones[hr_zone_start] = time_in_zones[hr_zone_start] + delta
            datetime_start = datetime_end
            hr_start = hr_end
    return time_in_zones


def get_heart_rate_zone(heart_rate_zones_dic, heart_rate):
    """
    Function that determines the zone of a given heart_rate
    """
    hr_result = ""
    hr_zones = heart_rate_zones_dic.keys()
    for hr_zone in hr_zones:
        [min, max] = heart_rate_zones_dic[hr_zone]
        if heart_rate >= min and heart_rate <= max:
            hr_result = hr_zone
            break
    return hr_result


def test_change_heart_rate_zone(heart_rate_zones_dic, hr_start, hr_end):
    """
    Function that determines whether there is a hr zone change
    """
    hr_zone_change = 0
    zone_start = get_heart_rate_zone(heart_rate_zones_dic, hr_start)
    zone_end = get_heart_rate_zone(heart_rate_zones_dic, hr_end)
    if zone_start != zone_end:
        hr_zone_change = 1
    return hr_zone_change


def sort_weeks(unsorted_week_list):
    """
    Function that sorts the week strings and returns a list of sorted weeks
    Input formate W10 - 6 Mar - 12 Mar
    """
    # FIX ME !!!
    unsorted_week_list_aux = []
    for week in unsorted_week_list:
        [aux1, aux2] = week.split("W") # split on W
        unsorted_week_list_aux.append(aux2) # aux2 has no W
    sorted_week_list = []
    for week in sorted(unsorted_week_list_aux):
        print(week)
        aux3 = "W" + week
        sorted_week_list.append(aux3)
    return sorted_week_list


def convert_speed_to_pace(speed_m_per_s):
    """
    Function that converts speed (m/s) to pace (min/km).
    If pace is to be printed then rest must be converted to seconds
    """
    dic_main = lib_conv.init()
    pace_min_km = lib_conv.conv(1/speed_m_per_s, "pace", "second/metre", "minute/kilometre", dic_main)
    return pace_min_km


def convert_speed_to_km_per_h(speed_m_per_s):
    """
    Function that converts speed in m/s to km/h
    """
    dic_main = lib_conv.init()
    speed_km_h = lib_conv.conv(speed_m_per_s, "speed", "metre/second", "kilometre/hour", dic_main)
    return speed_km_h

#----------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass