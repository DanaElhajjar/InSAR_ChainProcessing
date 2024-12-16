######################################################
#                    LIBRAIRIES                      #
######################################################

import os
import sys
from tqdm import trange
from utils import date_sort, checkDir

######################################################
#                USER PARAMETERS                     #
######################################################

#Path toward input images
pathInput = "" 

#Path to the output folder (interferograms) to be created
pathOutput_interferograms = "" 
pathOutput_coregistered = ""

#Path to the SNAP graph to be computed
pathSNAPGraph = ""

#Path to the gpt executable
pathGPT = ""

#Swath (bande) to be computed (one by one for memory issues)
swath = 3

#Delay between two radar images on which to compute interferogram
delay = 12

######################################################
#                   INITIALIZATION                   #
######################################################

# Find and sort SAR images to compute
liste_imgs_org = [f for f in os.listdir(pathInput) if not f.endswith(".data")]
liste_imgs_org = date_sort(liste_imgs_org)

#Check swath number
if swath not in [1,2,3]:
    print("Error : wrong swath number")
    sys.exit(1)

#Create output directory
checkDir(pathOutput_interferograms)
checkDir(pathOutput_coregistered)

#Number of successive images corresponding to the given delay
deltat=int(delay)//6

#Parameters for graphs configuration
gptConfigParams = ["product1", "product2", "outputFile_coregistered", "outputFile_interferograms", "swath1", "swath2"]

######################################################
#                   MAIN ROUTINE                     #
######################################################

for i in trange(1, len(liste_imgs_org)):
    print(pathInput)

    #Configuration of user parameters
    outputName_coregistered = f'{pathOutput_coregistered}/coregistrated_image_IW{swath}_VV_{0}_{i}.dim'
    outputName_interferograms = f'{pathOutput_interferograms}/ifg_IW{swath}_VV_{0}_{i}.dim'
    userParams = [pathInput + liste_imgs_org[0], pathInput+liste_imgs_org[i], outputName_coregistered , outputName_interferograms, str(swath), str(swath)]
    
    #Prepare command line
    comParams = ""
    for c, com in enumerate(gptConfigParams) :
        comParams += f"-P{com}={userParams[c]} "
    
    #Generate interferogram
    commandLine = f'{pathGPT} {pathSNAPGraph} {comParams}'
    os.system(commandLine)


######################################################
#                SAVE CONFIGURATION                  #
######################################################

#Path to the information file
pathInfo_interferograms = pathOutput_interferograms + 'interferograms_info.txt'
pathInfo_coregistered = pathOutput_coregistered + 'coregistered_images_info.txt'

#Open file and write data info
f= open(pathInfo_interferograms,"w+")
f.write("Path configuration")
f.write(f'Input path: {pathInput}\n')
f.write(f'Graph path: {pathSNAPGraph}\n')
f.write("Interferograms configuration")
f.write(f'Swath number: {swath}\n')
f.write(f"Delay: {delay}\n")
f.write("Corresponding Images")
for i, img in enumerate(liste_imgs_org):
    f.write(f"{i}: {img}")
f.close()

#Open file and write data info
f= open(pathInfo_coregistered,"w+")
f.write("Path configuration")
f.write(f'Input path: {pathInput}\n')
f.write(f'Graph path: {pathSNAPGraph}\n')
f.write("Coregistred images configuration")
f.write(f'Swath number: {swath}\n')
f.write(f"Delay: {delay}\n")
f.write("Corresponding Images")
for i, img in enumerate(liste_imgs_org):
    f.write(f"{i}: {img}")
f.close()
