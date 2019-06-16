# Background
Needed to develop a set of tools to help with planning and monitoring a sporting season using periodisation.


# Description
This repo contains tools that make planning and assessing the evolution of a sports season easier.

The tools require *.tcx* files of the activities. These files are generated from monitoring activities using sport watches (e.g. *Garmin Fenix 3*). They are *.xml* files in open format.

When using periodisation to plan a season, the ultimate goal is to reach peak performance in specific races. 

A high level description of each tool is given below:
1. **count_week_totals**: Reads the tcx files for a given week and returns the total amount of time spent in each activity type (e.g. running, cycling)

    *Inputs*: activities path, week
    
2. **print_week_activities_names**: Prints the activities names for a given week. This is used to get the name of a specific activity, which is then studied in more depth

    *Inputs*: activities path, week

3. **extract_activity_data**: Extracts useful info from an activity. An example is to extract the average speed and heart rate for the last 20 min of a race. 

    *Inputs*: activities path, week, heart_rate_dic, activity_name, delta_from_end_min

4. **count_commuting_savings**: Used to determine savings when commuting on a bike, ompared to using public transportation 

    *Inputs*: activities path, journey_price, travelcard_cap


## Output
All outputs are sent to the console output channel.

## Input data
- *activities path*: Path to the activities directory (use a slash in the end)
- *week*: string for the week (example format: W37 - 11 Jun - 17 Jun)

- *heart_rate_dic*:
    - Z1: list for zone 1 heart rate range
    - Z2: list for zone 2 heart rate range
    - Z3: list for zone 3 heart rate range
    - Z4: list for zone 4 heart rate range
    - Z5: list for zone 5 heart rate range

- *activity_name*: Activity name (e.g. Running on 16 June 2018 at 08:27:26)

- *delta_from_end_min*: delta time for activity analysis when extracting info from a specific activity (integer in min)

- *journey_price*: Journey price used to determine commuter savings (any real value in GBP)

- *travelcard_cap*: Value at which the costs of transportation are capped (any real value in GBP)

	
# Technologies used
Python3 including the libraries:

    - datetime
    - time
    - os
    - os.path
    - sys
    - bisect
    - math
    - lxml
    - yaml


# Status
This work is still in development.


# Known issues

# Future enhancements
1. Add sql connectivity
2. Improve inputs selection using a dialog box
3. Add more try / except and assert statements to improve robustness


# How to use it
1. Create a python 3 environment with the required libraries:
    - datetime
    - time
    - os
    - os.path
    - sys
    - bisect
    - math
    - lxml
    - yaml

2. Edit */inputs/inputs.yml* to point to the correct activities data location

3. Run *count_week_totals*, or any of the other scripts described above.

