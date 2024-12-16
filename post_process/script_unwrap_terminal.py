######################################################
#                    LIBRAIRIES                      #
######################################################

from imagesutils import modify_snaphu_file

######################################################
#                USER PARAMETERS                     #
######################################################

# the parent directory that contains all the subdirectories of the phase unwrapping results
father_folder = ""

# file .conf à to modify
conf_file = "snaphu.conf"

# keyword for the line that will be commented out 
comment_word = "LOGFILE"

if __name__=='main':
    modify_snaphu_file(father_folder,conf_file, comment_word )