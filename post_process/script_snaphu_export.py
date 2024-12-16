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
pathInput = ""

#Path to the output folder (unwrapped interferograms) to be created
pathOutput_unwrapped_interferograms = ""

#Path to the SNAP graph to be computed : snaphu_export
pathSNAPGraph = ""

#Path to the gpt executable
pathGPT = ""  

######################################################
#                   INITIALIZATION                   #
######################################################

# Find and sort SAR images to compute
liste_imgs_org = [f for f in os.listdir(pathInput) if not f.endswith(".data")]

# Trier la liste de fichiers en fonction des numéros extraits
liste_imgs_org = sorted(liste_imgs_org, key=extraire_numero)

#Create output directory
checkDir(pathOutput_unwrapped_interferograms)
# checkDir(pathOutput_unwrapped_interferograms_write)

#Parameters for graphs configuration
gptConfigParams = ["inputFile", "outputFolder_unwrapped_interferograms"]


######################################################
#                   MAIN ROUTINE                     #
######################################################

for i in trange(0, len(liste_imgs_org)):
    print(pathInput)

    #Configuration of user parameters
    inputFile = f"{pathInput}{liste_imgs_org[i]}"
    outputFolder_unwrapped_interferograms = f'{pathOutput_unwrapped_interferograms}/S_SG_MLE_PL_S1B_{i+1}_snaphu_export'
    userParams = [inputFile, outputFolder_unwrapped_interferograms]
    
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
pathInfo_unwrapped_interferograms = pathOutput_unwrapped_interferograms + 'unwrapped_interferograms_info.txt'

#Open file and write data info
f= open(pathInfo_unwrapped_interferograms,"w+")
f.write("Path configuration")
f.write(f'Input path: {pathInput}\n')
f.write(f'Graph path: {pathSNAPGraph}\n')
f.write("Corresponding Images")
for i, img in enumerate(liste_imgs_org):
    f.write(f"{i}: {img}")
f.close()