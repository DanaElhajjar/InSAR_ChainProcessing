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
    parser = argparse.ArgumentParser(description="Process SAR unwrapped interferograms using SNAP.")
    
    # Add required arguments
    parser.add_argument('--pathInput', type=str, required=True, help="Path to the input SAR images.")
    parser.add_argument('--pathOutput_unwrapped_interferograms', type=str, required=True, help="Path to output folder for unwrapped interferograms.")
    parser.add_argument('--pathSNAPGraph', type=str, required=True, help="Path to the SNAP graph to be used (snaphu_export).")
    parser.add_argument('--pathGPT', type=str, required=True, help="Path to the gpt executable.")
    parser.add_argument('--name_approach', type=str, required=True, help="Prefix for the output filenames (e.g., 'S_SG_MLE_PL').")
    
    # Parse and return the arguments
    return parser.parse_args()

######################################################
#                   MAIN FUNCTION                    #
######################################################

def main(args):
    """Main processing function."""
    
    # User parameters
    pathInput = args.pathInput
    pathOutput_unwrapped_interferograms = args.pathOutput_unwrapped_interferograms
    pathSNAPGraph = args.pathSNAPGraph
    pathGPT = args.pathGPT
    name_approach = args.name_approach  

    # Find and sort SAR images to process
    liste_imgs_org = [f for f in os.listdir(pathInput) if not f.endswith(".data")]

    # Sort the files based on extracted numbers
    liste_imgs_org = sorted(liste_imgs_org, key=extraire_numero)

    # Create output directory
    checkDir(pathOutput_unwrapped_interferograms)
    
    # Parameters for graph configuration
    gptConfigParams = ["inputFile", "outputFolder_unwrapped_interferograms"]
    
    # Main processing loop
    for i in trange(0, len(liste_imgs_org)):
        print(pathInput)

        # Configuration of user parameters
        inputFile = f"{pathInput}{liste_imgs_org[i]}"
        outputFolder_unwrapped_interferograms = f'{pathOutput_unwrapped_interferograms}/{name_approach}_S1B_{i+1}_snaphu_export'
        userParams = [inputFile, outputFolder_unwrapped_interferograms]
        
        # Prepare command line parameters
        comParams = ""
        for c, com in enumerate(gptConfigParams):
            comParams += f"-P{com}={userParams[c]} "
        
        # Generate unwrapped interferogram
        commandLine = f'{pathGPT} {pathSNAPGraph} {comParams}'
        os.system(commandLine)

    ######################################################
    #                SAVE CONFIGURATION                  #
    ######################################################

    # Path to the information file
    pathInfo_unwrapped_interferograms = pathOutput_unwrapped_interferograms + 'unwrapped_interferograms_info.txt'

    # Open file and write configuration information
    with open(pathInfo_unwrapped_interferograms, "w+") as f:
        f.write("Path configuration\n")
        f.write(f'Input path: {pathInput}\n')
        f.write(f'Graph path: {pathSNAPGraph}\n')
        f.write("Corresponding Images\n")
        for i, img in enumerate(liste_imgs_org):
            f.write(f"{i}: {img}\n")

######################################################
#                   ENTRY POINT                      #
######################################################

if __name__ == "__main__":
    # Parse the command-line arguments
    args = args_parse()

    # Call the main function with the parsed arguments
    main(args)
