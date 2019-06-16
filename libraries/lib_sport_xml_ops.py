# Metadata
#=========
__author__ = "Luis Domingues"
__maintainer__ = "Luis Domingues"
__email__ = "luis.hmd@gmail.com"

# Description
#============
# Library that provides xml operations


#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
from lxml import etree
ns = etree.FunctionNamespace(None)
ns['upper-case'] = lambda context, s: str.upper(s)
ns['lower-case'] = lambda context, s: str.lower(s)

import lib_datetime_ops as lib_datetime
import lib_sport_formatting as lib_sport_format


#----------------------------------------------------------------------------------------
# FUNCTIONS
#----------------------------------------------------------------------------------------
def parse_tree(input_xml):
    """
    Function that parses an <input> xml file and returns the parsed tree and its root
    """
    tree = None
    root = None
    try:
        tree = etree.parse(input_xml)
        root = tree.getroot()
    except:
        print("Could not parse XML tree for file <%s> (hint: possibly the model does not have a dialog)." %str(input_xml))
    return [tree, root]


def extract_activity_datetime(tree_root):
    """
    Function that returns the datetime object for when the activity starts
    """
    ns = {"url":"http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}
    try:
        activity_element_list = tree_root.findall(".//url:Activities/url:Activity", ns)
        date_time_element = activity_element_list[0].find("url:Id", ns) # There should always only be one activity
        datetime_obj = lib_datetime.create_datetime_object(date_time_element.text)
        return datetime_obj
    except:
        return 0


def extract_activity_totals(tree_root):
    """
    Function that returns the total activity time (s), distance (m) and calories (cal) for a given activity
    """
    laps_element_list = extract_activity_laps(tree_root)
    total_time_seconds = 0
    total_distance_metres = 0
    total_calories_cal = 0
    for lap_element in laps_element_list:
        [lap_total_time_seconds, lap_total_distance_metres, lap_total_calories_cal] = extract_lap_totals_tag_based(lap_element)
        # Option 1 for total time
        #total_time_seconds += lap_total_time_seconds
        total_distance_metres += lap_total_distance_metres
        total_calories_cal += lap_total_calories_cal
    # Option 2 for total time -> more accurate
    tp_element_list = extract_lap_trackpoints(laps_element_list[0])
    if tp_element_list:
        start_tp_elem = tp_element_list[0]
        tp_element_list = extract_lap_trackpoints(laps_element_list[len(laps_element_list)-1])
        end_tp_elem = tp_element_list[len(tp_element_list)-1]
        delta = extract_trackpoint_datetime(end_tp_elem) - extract_trackpoint_datetime(start_tp_elem)
        total_time_seconds = delta.total_seconds()
    else:
        print("Could not extract total time for activity <%s>" %(lib_sport_format.format_name_activity("Activity", extract_activity_datetime(tree_root))))
    return [total_time_seconds, total_distance_metres, total_calories_cal]


def extract_activity_maximums(tree_root):
    """
    Function that returns the maximum activity HR (bpm), speed (m/s) and cadence spm) as floats
    """
    laps_element_list = extract_activity_laps(tree_root)
    max_hr = 0
    max_speed = 0
    max_cadence = 0
    for lap_element in laps_element_list:
        [lap_max_hr, lap_max_speed, lap_max_cadence] = extract_lap_maximums(lap_element)
        if lap_max_hr > max_hr:
            max_hr = lap_max_hr
        if lap_max_speed > max_speed:
            max_speed = lap_max_speed
        if lap_max_cadence > max_cadence:
            max_cadence = lap_max_cadence
    return [max_hr, max_speed, max_cadence]


def extract_activity_laps(tree_root):
    """
    Function that returns the lap elements for a given activity
    """
    ns = {"url":"http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}
    try:
        laps_element_list = tree_root.findall(".//url:Activities/url:Activity/url:Lap", ns)
        return laps_element_list
    except:
        return []


def extract_activity_time_profiles(tree_root):
    """
    Function that returns the time profiles for the entire activity
    """
    laps_element_list = extract_activity_laps(tree_root)
    time = []
    heart_rate = []
    speed = []
    cadence = []
    latitude = []
    longitude = []
    altitude = []
    distance = []
    if laps_element_list:
        for lap_element in laps_element_list:
            # Extract time profiles
            [lap_time, lap_heart_rate, lap_speed, lap_cadence, lap_latitude, lap_longitude, lap_altitude, lap_distance] = extract_lap_time_profiles(lap_element)
            # May not have all the sensors
            for t in lap_time:
                time.append(t)
            # Heart rate
            for hr in lap_heart_rate:
                heart_rate.append(hr)
            # Speed
            for s in lap_speed:
                speed.append(s)
            # Cadence
            for cad in lap_cadence:
                cadence.append(cad)
            # Position
            for lat in lap_latitude:
                latitude.append(lat)
            for lon in lap_longitude:
                longitude.append(lon)
            # Altitude
            for alt in lap_altitude:
                altitude.append(alt)
            # Distance
            for dist in lap_distance:
                distance.append(dist)
    return [time , heart_rate, speed, cadence, latitude, longitude, altitude, distance]


def extract_lap_totals_tag_based(lap_element):
    """
    Function that returns the lap total time (s), the lap total distance (m) and the lap calories (cal) as floats, based on the lap total tags
    """
    ns = {"url":"http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}
    lap_total_time_seconds = 0
    lap_total_distance_metres = 0
    lap_total_calories_cal = 0
    # Try to get time
    try:
        lap_total_time_seconds_element = lap_element.find("url:TotalTimeSeconds", ns)
        lap_total_time_seconds = float(lap_total_time_seconds_element.text)
    except:
        print("Could not get lap total time.")
    # Try to get distance
    try:
        lap_total_distance_metre_element = lap_element.find("url:DistanceMeters", ns)
        lap_total_distance_metres = float(lap_total_distance_metre_element.text)
    except:
        print("Could not get lap total distance.")
    # Try to get calories
    try:
        lap_total_calories_cal_element = lap_element.find("url:Calories", ns)
        lap_total_calories_cal = float(lap_total_calories_cal_element.text)
    except:
        print("Could not get lap total calories.")
    return [lap_total_time_seconds, lap_total_distance_metres, lap_total_calories_cal]


def extract_lap_totals_trackpoint_based(lap_element):
    """
    Function that returns the lap total time (s), the lap total distance (m) and the lap calories (cal) as floats based on the trackpoints info
    """
    ns = {"url":"http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}
    lap_total_time_seconds = 0
    lap_total_distance_metres = 0
    lap_total_calories_cal = 0
    trackpoint_element_list = extract_lap_trackpoints(lap_element)
    # Try to get time
    if trackpoint_element_list:
        first_tp_elem = trackpoint_element_list[0]
        last_tp_elem = trackpoint_element_list[len(trackpoint_element_list)-1]
        delta = extract_trackpoint_datetime(last_tp_elem) - extract_trackpoint_datetime(first_tp_elem)
        lap_total_time_seconds = delta.total_seconds()
    else:
        print("Could not get lap total time.")
    # Try to get distance
    if trackpoint_element_list:
        first_tp_elem = trackpoint_element_list[0]
        last_tp_elem = trackpoint_element_list[len(trackpoint_element_list)-1]
        lap_total_distance_metres = extract_trackpoint_distance(last_tp_elem) - extract_trackpoint_distance(first_tp_elem)
    else:
        print("Could not get lap total distance.")
    # Try to get calories
    try:
        lap_total_calories_cal_element = lap_element.find("url:Calories", ns)
        lap_total_calories_cal = float(lap_total_calories_cal_element.text)
    except:
        print("Could not get lap total calories.")
    return [lap_total_time_seconds, lap_total_distance_metres, lap_total_calories_cal]


def extract_lap_averages(lap_element):
    """
    Function that returns the lap average HR (bpm), speed (m/s) and cadence spm) as floats
    """
    ns = {"url":"http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
          "url3": "http://www.garmin.com/xmlschemas/ActivityExtension/v2"}
    lap_avg_hr = 0
    lap_avg_speed = 0
    lap_avg_cadence = 0
    # Try to get HR
    try:
        lap_avg_hr_element = lap_element.find("url:AverageHeartRateBpm/url:Value", ns)
        lap_avg_hr = float(lap_avg_hr_element.text)
    except:
        print("Could not get lap average heart rate.")
    # Try to get speed
    try:
        lap_avg_speed_element = lap_element.find("url:Extensions/url3:LX/url3:AvgSpeed", ns)
        lap_avg_speed = float(lap_avg_speed_element.text)
    except:
        print("Could not get lap average speed.")
    # Try to get cadence
    try:
        lap_avg_cadence_element = lap_element.find("url:Extensions/url3:LX/url3:AvgRunCadence", ns)
        lap_avg_cadence = float(lap_avg_cadence_element.text)
    except:
        print("Could not get lap average cadence.")
    return [lap_avg_hr, lap_avg_speed, lap_avg_cadence]


def extract_lap_maximums(lap_element):
    """
    Function that returns the lap maximum HR (bpm), speed (m/s) and cadence spm) as floats
    """
    ns = {"url":"http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
          "url3": "http://www.garmin.com/xmlschemas/ActivityExtension/v2"}
    lap_max_hr = 0
    lap_max_speed = 0
    lap_max_cadence = 0
    # Try to get HR
    try:
        lap_max_hr_element = lap_element.find("url:MaximumHeartRateBpm/url:Value", ns)
        lap_max_hr = float(lap_max_hr_element.text)
    except:
        print("Could not get lap maximum heart rate.")
    # Try to get speed
    try:
        lap_max_speed_element = lap_element.find("url:MaximumSpeed", ns)
        lap_max_speed = float(lap_max_speed_element.text)
    except:
        print("Could not get lap maximum speed.")
    # Try to get cadence
    try:
        lap_max_cadence_element = lap_element.find("url:Extensions/url3:LX/url3:MaxRunCadence", ns)
        lap_max_cadence = float(lap_max_cadence_element.text)
    except:
        print("Could not get lap maximum cadence.")
    return [lap_max_hr, lap_max_speed, lap_max_cadence]


def extract_lap_trackpoints(lap_element):
    """
    Function that returns the lap elements for a given activity
    """
    ns = {"url":"http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}
    try:
        trackpoint_element_list = lap_element.findall("url:Track/url:Trackpoint", ns)
        return trackpoint_element_list
    except:
        return []


def extract_lap_time_profiles(lap_element):
    """
    Function that returns the lap time profiles
    """
    time = []
    heart_rate = []
    speed = []
    cadence = []
    latitude = []
    longitude = []
    altitude = []
    distance = []
    trackpoint_element_list = extract_lap_trackpoints(lap_element)
    if trackpoint_element_list:
        for trackpoint_element in trackpoint_element_list:
            # Time
            time_aux = extract_trackpoint_datetime(trackpoint_element)
            time.append(time_aux)
            # Heart rate
            heart_rate_value_aux = extract_trackpoint_heart_rate(trackpoint_element)
            heart_rate.append(heart_rate_value_aux)
            # Speed
            speed_value_aux = extract_trackpoint_speed(trackpoint_element)
            speed.append(speed_value_aux)
            # Cadence
            cadence_value_aux = extract_trackpoint_cadence(trackpoint_element)
            cadence.append(cadence_value_aux)
            # Position
            [latitude_value_aux, longitude_value_aux] = extract_trackpoint_position(trackpoint_element)
            latitude.append(latitude_value_aux)
            longitude.append(longitude_value_aux)
            # Altitude
            altitude_value_aux = extract_trackpoint_altitude(trackpoint_element)
            altitude.append(altitude_value_aux)
            # Distance
            distance_value_aux = extract_trackpoint_distance(trackpoint_element)
            distance.append(distance_value_aux)
    return [time, heart_rate, speed, cadence, latitude, longitude, altitude, distance]


def extract_trackpoint_datetime(trackpoint_element):
    """
    Function that returns the datetime object of a given trackpoint element
    Input format is YYYY-MM-DDThh:mm:ss.000Z
    """
    ns = {"url":"http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}
    try:
        date_time_element = trackpoint_element.find("url:Time", ns)
        datetime_obj = lib_datetime.create_datetime_object(date_time_element.text)
        return datetime_obj
    except:
        return 0


def extract_trackpoint_heart_rate(trackpoint_element):
    """
    Function that returns the heart rate as an integer of a given trackpoint element
    """
    ns = {"url":"http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}
    try:
        heart_rate_value_element = trackpoint_element.find("url:HeartRateBpm/url:Value", ns)
        return int(heart_rate_value_element.text)
    except:
        return 0


def extract_trackpoint_speed(trackpoint_element):
    """
    Function that returns the speed as a float of a given trackpoint element
    """
    ns = {"url":"http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
          "url3": "http://www.garmin.com/xmlschemas/ActivityExtension/v2"}
    try:
        speed_element = trackpoint_element.find("url:Extensions/url3:TPX/url3:Speed", ns)
        return float(speed_element.text)
    except:
        return 0


def extract_trackpoint_cadence(trackpoint_element):
    """
    Function that returns the cadence as an integer of a given trackpoint element
    """
    ns = {"url":"http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
          "url3": "http://www.garmin.com/xmlschemas/ActivityExtension/v2"}
    try:
        cadence_element = trackpoint_element.find("url:Cadence", ns) # cycling first
        return int(cadence_element.text)
    except:
        try:
            cadence_element = trackpoint_element.find("url:Extensions/url3:TPX/url3:RunCadence", ns) # running
            return int(cadence_element.text)
        except:
            return 0


def extract_trackpoint_position(trackpoint_element):
    """
    Function that returns the position as a list [Lat, Long] of floats of a given trackpoint
    """
    ns = {"url":"http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}
    try:
        latitude_value_element = trackpoint_element.find("url:Position/url:LatitudeDegrees", ns)
        longitude_value_element = trackpoint_element.find("url:Position/url:LongitudeDegrees", ns)
        return [float(latitude_value_element.text), float(longitude_value_element.text)]
    except:
        return [0, 0]


def extract_trackpoint_altitude(trackpoint_element):
    """
    Function that returns the altitude as a float of a given trackpoint
    """
    ns = {"url":"http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}
    try:
        altitude_value_element = trackpoint_element.find("url:AltitudeMeters", ns)
        return float(altitude_value_element.text)
    except:
        return 0


def extract_trackpoint_distance(trackpoint_element):
    """
    Function that returns the distance as a float of a given trackpoint
    """
    ns = {"url": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}
    try:
        distance_value_element = trackpoint_element.find("url:DistanceMeters", ns)
        return float(distance_value_element.text)
    except:
        return 0


#----------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass