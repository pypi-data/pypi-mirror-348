# Use the rawdata folder to store all experimental data. ONLY!!!!.
Copy the following text into a notebook:

from arenz_group_python import Project_Paths

pp = Project_Paths()
project_name = 'projectname'
user_initials = '' #This is optional, but it can speed up things
path_to_server = 'X:/EXP_DB'
pp.copyDirs(path_to_server, user_initials , project_name )
