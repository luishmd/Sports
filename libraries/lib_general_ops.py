# Metadata
#=========
__author__ = "Luis Domingues"
__maintainer__ = "Luis Domingues"
__email__ = "luis.hmd@gmail.com"

# Description
#============
# Library that provides general operations


#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
import sys
import bisect as bisect


#----------------------------------------------------------------------------------------
# FUNCTIONS
#----------------------------------------------------------------------------------------
def append_list(list_main, list_append):
    """
    Function that appends a list to another list
    """
    for element in list_append:
        list_main.append(element)
    return list_main


def convert_list_to_set(input_list):
    """
    Function that converts a list to a set. The return type is a list
    """
    output = list(set(input_list))
    return output


def convert_list_to_lowercase(input_list):
    """
    Function that converts all elements in a list of strings to lower_case
    """
    output = [element.lower() for element in input_list]
    return output


def get_duplicates(input_list):
    """
    Function that returns the duplicates in input_list
    """
    duplicates = []
    input_set = convert_list_to_set(input_list)
    if len(input_list) != len(input_set):
        duplicates = list(set([x for x in input_list if input_list.count(x) > 1]))
    return duplicates


def get_list_difference(main_list, list_to_subtract):
    """
    Function that returns the list that is the difference between a main list and a list_to_subtract (result = main_list - list_to_subtract)
    """
    result = []
    for element in main_list:
        if not element in list_to_subtract:
            result.append(element)
    return result


def print2file(file_path):
    """
    Function that resets stdout to write to file
    """
    sys.stdout = open(file_path,"w")


def get_index_in_list(ordered_list, value):
    """
    Function that returns the index in the ordered_list of the element before value
    """
    index = bisect.bisect_left(ordered_list, value)
    return index


#----------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass