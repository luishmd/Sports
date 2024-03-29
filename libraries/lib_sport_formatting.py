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
import lib_datetime_ops as lib_datetime


#----------------------------------------------------------------------------------------
# FUNCTIONS
#----------------------------------------------------------------------------------------
def format_name_activity(sport_type_str, datetime_obj):
    """
    Function that returns a string corresponding to the standard for the name of an activity
    """
    return sport_type_str + " on " + lib_datetime.format_date(datetime_obj) + " at " + lib_datetime.format_time(datetime_obj)


#----------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass