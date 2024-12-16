######################################################
#                    LIBRAIRIES                      #
######################################################
import os
import sys
from tqdm import trange
from imagesutils import (extraire_numero, 
                         checkDir)

######################################################
#                USER PARAMETERS                     #
######################################################

# Path toward input images (estimated interferogram)
pathInput1 = ""
# Path toward input images (unwrapped estimated interferogram)
pathInput2 =  ""

#Path to the output folder (unwrapped interferograms) to be created
pathOutput_displacement = ""

#Path to the SNAP graph to be computed : displacement_map.xml
pathSNAPGraph = ""

#Path to the gpt executable
pathGPT = ""  
######################################################
#                   INITIALIZATION                   #
######################################################

# Find and sort wrapped interferograms
list_wrapped_interfero = [f for f in os.listdir(pathInput1) if not f.endswith(".data")]
# Trier la liste de fichiers en fonction des numéros extraits
list_wrapped_interfero = sorted(list_wrapped_interfero, key=extraire_numero)

# Find and sort unwrapped interferograms
list_unwrapped_interfero = [f for f in os.listdir(pathInput2)]
# Trier la liste de fichiers en fonction des numéros extraits
list_unwrapped_interfero = sorted(list_unwrapped_interfero, key=extraire_numero)

#Create output directory
checkDir(pathOutput_displacement)

#Parameters for graphs configuration
gptConfigParams = ["inputFile1", "inputFile2", "outputFile_displacement_write"]

######################################################
#                   MAIN ROUTINE                     #
######################################################

for i in trange(0, len(list_wrapped_interfero)):
    print("path for wrapped interferograms: ", pathInput1)
    print("path for unwrapped interferograms: ", pathInput2)

    #Configuration of user parameters
    inputFile1 = f"{pathInput1}{list_wrapped_interfero[i]}"
    inputFile2 = f"{pathInput2}{list_unwrapped_interfero[i]}/UnwS_SG_MLE_PL_date_{i+1}_phase.snaphu.hdr"
    outputFile_displacement_write = f'{pathOutput_displacement}/S_SG_MLE_PL_{i+1}_displacement_snaphu_import.dim'
    userParams = [inputFile1, inputFile2, outputFile_displacement_write]
    
    #Prepare command line
    comParams = ""
    for c, com in enumerate(gptConfigParams) :
        comParams += f"-P{com}={userParams[c]} "
    
    #Generate unwrapped interferogram
    commandLine = f'{pathGPT} {pathSNAPGraph} {comParams}'
    os.system(commandLine)

######################################################
#                SAVE CONFIGURATION                  #
######################################################

#Path to the information file
pathInfo_unwrapped_interferograms = pathOutput_displacement + 'displacement_info.txt'

#Open file and write data info
f= open(pathInfo_unwrapped_interferograms,"w+")
f.write("Path configuration")
f.write(f'Input path for wrapped interferograms: {pathInput1}\n')
f.write(f'Input path for unwrapped interferograms: {pathInput2}\n')
f.write(f'Graph path: {pathSNAPGraph}\n')
f.write("Corresponding Images")
for i, img in enumerate(list_wrapped_interfero):
    f.write(f"{i}: {img}")
f.close()