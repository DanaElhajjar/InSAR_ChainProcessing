######################################################
#                    LIBRAIRIES                      #
######################################################

import os
import sys
from tqdm import trange
from utils import date_sort, checkDir
import argparse

######################################################
#                USER PARAMETERS                     #
######################################################

def parse_arguments():
    parser = argparse.ArgumentParser(description="Script pour le traitement des images SAR")
    
    # Définition des arguments
    parser.add_argument('--pathInput', type=str, required=True, 
                        help="Chemin vers les images SAR brutes (input)")
    parser.add_argument('--pathOutput_interferograms', type=str, required=True, 
                        help="Chemin vers le dossier de sortie pour les interférogrammes")
    parser.add_argument('--pathOutput_coregistered', type=str, required=True, 
                        help="Chemin vers le dossier de sortie pour les images coregistrées")
    parser.add_argument('--pathSNAPGraph', type=str, required=True, 
                        help="Chemin vers le graphique SNAP à calculer")
    parser.add_argument('--pathGPT', type=str, required=True, 
                        help="Chemin vers l'exécutable GPT de SNAP")
    parser.add_argument('--swath', type=int, default=3, 
                        help="Numéro de la bande (swath) à traiter, un par un pour les problèmes de mémoire (par défaut: 3)")
    parser.add_argument('--delay', type=int, default=12, 
                        help="Délai entre deux images radar pour calculer l'interférogramme (par défaut: 12)")

    return parser.parse_args()

######################################################
#                   INITIALIZATION                   #
######################################################

def main():
    # Parse les arguments de la ligne de commande
    args = parse_arguments()

    # Initialisation des paramètres utilisateur
    pathInput = args.pathInput
    pathOutput_interferograms = args.pathOutput_interferograms
    pathOutput_coregistered = args.pathOutput_coregistered
    pathSNAPGraph = args.pathSNAPGraph
    pathGPT = args.pathGPT
    swath = args.swath
    delay = args.delay

    # Find and sort SAR images to compute
    liste_imgs_org = [f for f in os.listdir(pathInput) if not f.endswith(".data")]
    liste_imgs_org = date_sort(liste_imgs_org)

    # Check swath number
    if swath not in [1, 2, 3]:
        print("Error: wrong swath number")
        sys.exit(1)

    # Create output directory
    checkDir(pathOutput_interferograms)
    checkDir(pathOutput_coregistered)

    # Number of successive images corresponding to the given delay
    deltat = int(delay) // 6

    # Parameters for graphs configuration
    gptConfigParams = ["product1", "product2", "outputFile_coregistered", "outputFile_interferograms", "swath1", "swath2"]

    ######################################################
    #                   MAIN ROUTINE                     #
    ######################################################

    for i in trange(1, len(liste_imgs_org)):
        print(pathInput)

        # Configuration of user parameters
        outputName_coregistered = f'{pathOutput_coregistered}/coregistrated_image_IW{swath}_VV_{0}_{i}.dim'
        outputName_interferograms = f'{pathOutput_interferograms}/ifg_IW{swath}_VV_{0}_{i}.dim'
        userParams = [pathInput + liste_imgs_org[0], pathInput + liste_imgs_org[i], outputName_coregistered , outputName_interferograms, str(swath), str(swath)]

        # Prepare command line
        comParams = ""
        for c, com in enumerate(gptConfigParams):
            comParams += f"-P{com}={userParams[c]} "

        # Generate interferogram
        commandLine = f'{pathGPT} {pathSNAPGraph} {comParams}'
        os.system(commandLine)

    ######################################################
    #                SAVE CONFIGURATION                  #
    ######################################################

    # Path to the information file
    pathInfo_interferograms = pathOutput_interferograms + 'interferograms_info.txt'
    pathInfo_coregistered = pathOutput_coregistered + 'coregistered_images_info.txt'

    # Open file and write data info
    with open(pathInfo_interferograms, "w+") as f:
        f.write("Path configuration\n")
        f.write(f'Input path: {pathInput}\n')
        f.write(f'Graph path: {pathSNAPGraph}\n')
        f.write("Interferograms configuration\n")
        f.write(f'Swath number: {swath}\n')
        f.write(f"Delay: {delay}\n")
        f.write("Corresponding Images\n")
        for i, img in enumerate(liste_imgs_org):
            f.write(f"{i}: {img}\n")

    # Open file and write data info
    with open(pathInfo_coregistered, "w+") as f:
        f.write("Path configuration\n")
        f.write(f'Input path: {pathInput}\n')
        f.write(f'Graph path: {pathSNAPGraph}\n')
        f.write("Coregistred images configuration\n")
        f.write(f'Swath number: {swath}\n')
        f.write(f"Delay: {delay}\n")
        f.write("Corresponding Images\n")
        for i, img in enumerate(liste_imgs_org):
            f.write(f"{i}: {img}\n")

if __name__ == "__main__":
    main()