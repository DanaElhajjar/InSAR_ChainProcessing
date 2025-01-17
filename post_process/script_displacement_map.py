######################################################
#                    LIBRARIES                      #
######################################################

import os
import sys
from tqdm import trange
from imagesutils import (extraire_numero, 
                         checkDir)
import argparse

######################################################
#                FUNCTION TO PARSE ARGUMENTS          #
######################################################

def args_parse():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate displacement maps from wrapped and unwrapped interferograms.")
    
    # Add required arguments
    parser.add_argument('--pathInput1', type=str, required=True, help="Path to input wrapped interferograms.")
    parser.add_argument('--pathInput2', type=str, required=True, help="Path to input unwrapped interferograms.")
    parser.add_argument('--pathOutput_displacement', type=str, required=True, help="Path to output folder for displacement maps.")
    parser.add_argument('--pathSNAPGraph', type=str, required=True, help="Path to the SNAP graph (displacement_map.xml).")
    parser.add_argument('--pathGPT', type=str, required=True, help="Path to the gpt executable.")
    parser.add_argument('--name_approach', type=str, required=True, help="Prefix for the output filenames (e.g., 'S_SG_MLE_PL').")
    
    # Parse and return the arguments
    return parser.parse_args()

######################################################
#                   MAIN FUNCTION                    #
######################################################

def main(args):
    """Main processing function to generate displacement maps."""
    
    # User parameters
    pathInput1 = args.pathInput1
    pathInput2 = args.pathInput2
    pathOutput_displacement = args.pathOutput_displacement
    pathSNAPGraph = args.pathSNAPGraph
    pathGPT = args.pathGPT
    name_approach = args.name_approach  # This is the new variable for custom filename prefix
    
    # Find and sort wrapped interferograms
    list_wrapped_interfero = [f for f in os.listdir(pathInput1) if not f.endswith(".data")]
    list_wrapped_interfero = sorted(list_wrapped_interfero, key=extraire_numero)

    # Find and sort unwrapped interferograms
    list_unwrapped_interfero = [f for f in os.listdir(pathInput2)]
    list_unwrapped_interfero = sorted(list_unwrapped_interfero, key=extraire_numero)

    # Create output directory
    checkDir(pathOutput_displacement)

    # Parameters for graph configuration
    gptConfigParams = ["inputFile1", "inputFile2", "outputFile_displacement_write"]

    # Main processing loop
    for i in trange(0, len(list_wrapped_interfero)):
        print("Path for wrapped interferograms: ", pathInput1)
        print("Path for unwrapped interferograms: ", pathInput2)

        # Configuration of user parameters
        inputFile1 = f"{pathInput1}{list_wrapped_interfero[i]}"
        inputFile2 = f"{pathInput2}{list_unwrapped_interfero[i]}/Unw{ name_approach }_date_{i+1}_phase.snaphu.hdr"
        outputFile_displacement_write = f'{pathOutput_displacement}/{name_approach}_{i+1}_displacement_snaphu_import.dim'
        userParams = [inputFile1, inputFile2, outputFile_displacement_write]
        
        # Prepare command line parameters
        comParams = ""
        for c, com in enumerate(gptConfigParams):
            comParams += f"-P{com}={userParams[c]} "
        
        # Generate displacement map
        commandLine = f'{pathGPT} {pathSNAPGraph} {comParams}'
        os.system(commandLine)

    ######################################################
    #                SAVE CONFIGURATION                  #
    ######################################################

    # Path to the information file
    pathInfo_unwrapped_interferograms = pathOutput_displacement + 'displacement_info.txt'

    # Open file and write configuration information
    with open(pathInfo_unwrapped_interferograms, "w+") as f:
        f.write("Path configuration\n")
        f.write(f'Input path for wrapped interferograms: {pathInput1}\n')
        f.write(f'Input path for unwrapped interferograms: {pathInput2}\n')
        f.write(f'Graph path: {pathSNAPGraph}\n')
        f.write("Corresponding Images\n")
        for i, img in enumerate(list_wrapped_interfero):
            f.write(f"{i}: {img}\n")

######################################################
#                   ENTRY POINT                      #
######################################################

if __name__ == "__main__":
    # Parse the command-line arguments
    args = args_parse()

    # Call the main function with the parsed arguments
    main(args)
