######################################################
#                    LIBRARIES                      #
######################################################

from imagesutils import modify_snaphu_file
import argparse
import os

######################################################
#                FUNCTION TO PARSE ARGUMENTS          #
######################################################

def args_parse():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Modify the snaphu configuration file by commenting out a specific line.")
    
    # Add required arguments
    parser.add_argument('--father_folder', type=str, required=True, help="The parent directory that contains all the subdirectories of the phase unwrapping results.")
    parser.add_argument('--conf_file', type=str, default="snaphu.conf", help="The .conf file to modify (default is 'snaphu.conf').")
    parser.add_argument('--comment_word', type=str, required=True, help="The keyword for the line that will be commented out.")
    
    # Parse and return the arguments
    return parser.parse_args()

######################################################
#                   MAIN FUNCTION                    #
######################################################

def main(args):
    """Main processing function to modify the snaphu configuration file."""
    
    # User parameters
    father_folder = args.father_folder
    conf_file = args.conf_file
    comment_word = args.comment_word
    
    # Ensure the father_folder exists
    if not os.path.isdir(father_folder):
        print(f"Error: The directory {father_folder} does not exist.")
        return

    # Modify the snaphu configuration file by commenting out the line containing the keyword
    modify_snaphu_file(father_folder, conf_file, comment_word)

######################################################
#                   ENTRY POINT                      #
######################################################

if __name__ == "__main__":
    # Parse the command-line arguments
    args = args_parse()

    # Call the main function with the parsed arguments
    main(args)
