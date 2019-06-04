__author__ = 'luisd'

#----------------------------------------------------------------------------------------
# Notes
#----------------------------------------------------------------------------------------


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

#----------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------
weeks_names = lib_sports.get_names_weeks(root_dir)
week_savings_dic = {}
total_savings = 0
for week in weeks_names:
    week_savings_dic[week] = lib_sports.calc_savings_week_commute(root_dir, week+"/")
    total_savings += week_savings_dic[week]

# Print results
lib_print.print_commuting_savings(week_savings_dic, total_savings)