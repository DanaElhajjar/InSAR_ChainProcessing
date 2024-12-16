
# -----------------------------------------------------------------
# Librairies
# -----------------------------------------------------------------

import numpy as np
import struct
import os 
import re
import subprocess

# -----------------------------------------------------------------
# Functions
# -----------------------------------------------------------------

def writehdrfile(shape1,shape2,bandname,filename,unit):
    """A function that generates an ENVI header (.hdr) file with the specified metadata.

    Input:
        * shape1 (int): Number of lines (rows) in the image (vertical dimension)
        * shape2 (int): Number of samples (columns) per line in the image (horizontal dimension)
        * bandname (str): Name of the spectral band or associated description 
        * filename (str): Nname of the header file to be created (.hdr)
        * unit (str): Unit of the data (e.g., "phase", "coherence")
    """
    with open(filename,'w+') as f:
        line1 = 'ENVI \n'
        line2 = 'description = {Sentinel-1 IW Level-1 SLC Product - Unit: '+unit+'} \n'
        line3 = 'samples = '+str(shape2)+' \n'
        line4 = 'lines = '+str(shape1)+ ' \n'
        line5 = 'bands = 1 \n'
        line6 = 'header offset = 0 \n'
        line7 = 'file type = ENVI Standard \n'
        line8 = 'data type = 4 \n'
        line9 = 'interleave = bsq \n'
        line10 = 'byte order = 1 \n'
        line11 = 'band names = { '+bandname+' } \n'
        line12 = 'data gain values = {1.0} \n'
        line13 = 'data offset values = {0.0} \n'
        f.writelines([line1,line2,line3,line4,line5,line6,line7,line8,line9,line10,line11,line12,line13])
        f.close()


def save_float(path, targetsz, array):
    """ A function that generates an ENVI header (.img) file with the specified .hdr file

    Input:
        path (str): path and name of the output (.img)
        targetsz (tuple): size of the data vector
        array (Numpy array): array of the data
    """

    
    originsz = array.shape 

    firstpadding = np.ones([targetsz[0]-originsz[0],originsz[1]])*np.nan
    secondpadding = np.ones([targetsz[0],targetsz[1]-originsz[1]])*np.nan

    temp = np.concatenate((array,firstpadding),axis=0)
    finalimg = np.concatenate((temp,secondpadding),axis=1)
    array = finalimg.flatten()
    b = struct.pack('>'+'f'*len(array), *array)
    with open(path, "wb") as file:
        file.write(b)

def coherence_normalization(correlation_matrix):
    """ A function that computes the coherence matrix using the correlation matrix
    
    Input:
        * correlation_matrix (Numpy array): correlation matrix of the data
    Output:
        * coherence_matrix (Numpy array): coherence matrix of the data
    """
    p = correlation_matrix.shape[0]
    coherence_matrix = np.zeros((p, p))
    for i in range(p):
        for j in range(p):
            coherence_matrix[i, j] = correlation_matrix[i, j] / (np.sqrt(correlation_matrix[i, i]) * np.sqrt(correlation_matrix[j, j]))
    return coherence_matrix


def extraire_numero(filename):
    """
    A function that extracts the numeric part from a given filename after the string "_S1B_".
    
    Input: 
        * filename (str) - The filename from which the number will be extracted.
    
    Output:
        * (int) - The extracted number after "_S1B_" if found; otherwise, returns a very large value (infinity).
    """
    # Rechercher le chiffre dans le nom (après "S1B_")
    match = re.search(r"_S1B_(\d+)", filename)
    if match:
        return int(match.group(1))
    return float('inf')  # Valeur très grande si aucun chiffre n'est trouvé

def checkDir(path):
    """
    A function that checks if directory already exists and create it
    
    Input:
        * path : Path to be checked
    """

    #Check if the path exists
    if not os.path.exists(path):
        #Recreate it empty
        os.mkdir(path)

def modify_snaphu_file(father_folder, conf_file, comment_word):
    """
    A function that traverses all subdirectories within a parent folder, checks if a specific .conf file exists in each subdirectory, 
    modifies the content of the .conf file by commenting out specific lines, and executes a command if found.
    
    It performs the following steps:
    1. Traverses all subdirectories in the specified parent folder.
    2. For each subdirectory, checks if the .conf file exists.
    3. Reads the .conf file, modifies it by commenting out a specific line, and updates the file.
    4. Extracts and executes a 'snaphu' command if found in the file.

    Input:
        * father_folder (str) : the parent directory that contains all the subdirectories of the phase unwrapping results
        * conf_file (str) :  file .conf à to modify
        * comment_word (str) : keyword for the line that will be commented out
    """
    #Traverse all subdirectories in the parent folder
    for root, dirs, files in os.walk(father_folder):
        for dossier in dirs:
            chemin_dossier = os.path.join(root, dossier)  # Get the path to the corresponding subdirectory
            chemin_fichier_conf = os.path.join(chemin_dossier, conf_file)  # Path to the .conf file in the subdirectory

            # Check if the .conf file exists
            if os.path.exists(chemin_fichier_conf):
                print(f"Traitement du fichier : {chemin_fichier_conf}")

                # Read the content of the .conf file
                with open(chemin_fichier_conf, "r") as fichier:
                    lignes = fichier.readlines()

                # Modify the file
                lignes_modifiees = []
                commande = None
                for ligne in lignes:
                    # If the line contains the keyword to comment out, comment it
                    if comment_word in ligne and not ligne.strip().startswith("#"):
                        lignes_modifiees.append(f"# {ligne}")
                    # If the line contains the snaphu command, extract it
                    if "snaphu -f" in ligne:
                        # Extract elements of the command using a regular expression
                        match = re.search(r"snaphu -f snaphu.conf S_SG_MLE_PL_date_(\d+)_phase.snaphu.img (\d+)", ligne)
                        if match:
                            # Dynamically modify the command with the extracted number
                            i = match.group(1)
                            yyyy = match.group(2)
                            commande = f"snaphu -f snaphu.conf S_SG_MLE_PL_date_{i}_phase.snaphu.img {yyyy}"
                            lignes_modifiees.append(ligne)  # Keep the line without modification in the file
                    else:
                        lignes_modifiees.append(ligne)

                # Save the modifications to the file
                with open(chemin_fichier_conf, "w") as fichier:
                    fichier.writelines(lignes_modifiees)
                
                print(f"Ligne commentée et fichier mis à jour : {chemin_fichier_conf}")

                print(f"Line commented and file updated: {chemin_fichier_conf}")

                # Execute the command if it was found
                if commande:
                    print(f"Executing the command: {commande}")
                    subprocess.run(commande, shell=True, cwd=chemin_dossier)
                else:
                    print(f"No command found to execute in: {chemin_dossier}")
            else:
                print(f"File {conf_file} not found in: {chemin_dossier}")