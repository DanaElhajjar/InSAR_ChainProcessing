###################################################################
# packages
###################################################################
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
import argparse
import glob
import shutil
import os
import struct
import argparse
from utils import (splitdate,
                   modifyDIM,
                   list_file,
                   get_ncols_nrows_from_directory)

###################################################################
# functions
###################################################################
# Function to parse arguments
def parse_args():
    """Parses command-line arguments for the sigma matrix file and the output file.
    
    Input:
        * None
    
    Output:
        * args: Namespace object containing parsed command-line arguments.
    """
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Process SAR phase and coherence data.")

    # Add arguments to the parser
    parser.add_argument('--coregfolder', type=str, default="/home/elhajjad/PhD_Dana_NAS_share/elhajjad/output/coregistration/",
                        help="Path to the coregistration folder.")
    parser.add_argument('--name_approach', type=str, required=True, help="Name of the approach used in processing.")
    parser.add_argument('--input_path', type=str, required=True, 
                        help="Path to the input dataset folder containing the .dim files.")
    parser.add_argument('--path_hdr_img', type=str, required=True,
                        help="Path to input dataset folder containing the .hdr files.")
    parser.add_argument('--output_path', type=str, required=True, 
                        help="Path to the output folder where results will be saved.")
    parser.add_argument('--tempratio', type=int, default=1, 
                        help="Ratio for the temporary processing (default is 1).")
    parser.add_argument('--n_images', type=int, required=True, 
                        help="Number of images to process.")
    # parser.add_argument('--lamda', type=float, required=True, 
    #                     help="Lambda parameter used in processing.")
    # parser.add_argument('--p', type=int, required=True, 
    #                     help="P parameter used in processing.")
    # parser.add_argument('--name_approach', type=str, default="DSCOFIPL", 
    #                     help="Name of the approach used in processing (default is DSCOFIPL).")
    return parser.parse_args()

def main():
    # Parse the command-line arguments
    args = parse_args()
    
    # Use parsed arguments
    coregfolder = args.coregfolder
    name_approach = args.name_approach
    path_hdr_img = args.path_hdr_img
    listdim = list_file(args.input_path, '.dim')
    namedim = list_file(args.input_path, '.dim', base_name=True)

    # Derived variables
    tempratio = args.tempratio
    # name_approach = f"{args.name_approach}_nimages={args.n_images}_lambda={args.lamda}_p={args.p}_date_"
    tempbaseline = len(listdim)
    numberofimages = int(tempbaseline / tempratio)

    namedata = [namedim[i].replace('dim', 'data') for i in range(0, tempbaseline, tempratio)]

    # Get dates
    listdateful = splitdate(listdim[0:tempbaseline:tempratio][0:], 'ifg_IW3_VV_0_')

    # Paths
    pathout_SAR_phase = os.path.join(args.output_path, 'toSAR/SAR/')
    pathnoNaN = args.input_path  # Input path for the dataset

    # Get phase and coherence files
    listphase = glob.glob(path_hdr_img + name_approach + "*_phase.hdr")
    listphase.sort()
    print(listphase)

    listcoherence = glob.glob(path_hdr_img + name_approach + '*_coherence.hdr')
    listcoherence.sort()
    print(listcoherence)

    ncols, nrows = get_ncols_nrows_from_directory(path_hdr_img)

    ###################################################################
    # Processing Loop
    ###################################################################

    # Copy files and modify .dim files
    for i in range(0, tempbaseline):
        shutil.copytree(pathnoNaN + namedata[i], pathout_SAR_phase + namedata[i])  # Copy the .data directory
        shutil.copy(listdim[i], pathout_SAR_phase)  # Copy the .dim file
        
        # Create new file paths
        dstfd = os.path.join(pathout_SAR_phase, namedata[i])
        dst = os.path.join(pathout_SAR_phase, namedim[i])
        newname = name_approach + listdateful[i]
        newdstfd = os.path.join(pathout_SAR_phase, newname + '.data')
        newdst = os.path.join(pathout_SAR_phase, newname + '.dim')
        
        # Rename the files
        os.rename(dstfd, newdstfd)
        os.rename(dst, newdst)
        
        # Modify the .dim file
        os.chdir(pathout_SAR_phase)
        modifyDIM(pathout_SAR_phase, newname, listdateful[i], ncols, nrows, name_approach)

    # Handle phase and coherence files
    for i in range(0, tempbaseline):
        pathdata = os.path.join(pathout_SAR_phase, name_approach + listdateful[i] + '.data/')
        
        # Get the i, q, and coherence files
        listi = glob.glob(pathdata + 'i_ifg*')
        listq = glob.glob(pathdata + 'q_ifg*')
        list_coh = glob.glob(pathdata + 'coh_IW3*')
        
        # Remove old files
        for temp in range(len(listi)):
            print('temp = ', temp, 'listi=', listi[temp])
            os.remove(listi[temp])
            os.remove(listq[temp])
            os.remove(list_coh[temp])
        
        # Copy the new phase and coherence files
        shutil.copy(path_hdr_img + name_approach + listdateful[i] + '_phase.img', pathdata)
        shutil.copy(path_hdr_img + name_approach + listdateful[i] + '_phase.hdr', pathdata)
        shutil.copy(path_hdr_img + name_approach + listdateful[i] + '_coherence.img', pathdata)
        shutil.copy(path_hdr_img + name_approach + listdateful[i] + '_coherence.hdr', pathdata)


if __name__ == "__main__":
    main()


# python conv_to_SAR.py --input_path /path/to/your/dataset/ --path_hdr_img /path/to/your/hdr/ --output_path /path/to/output/ --n_images 10 --name_approach name
# python conv_to_SAR.py --input_path "/home/elhajjad/PhD_Dana_NAS_share/elhajjad/dataset_20_interfero/" \
#     --path_hdr_img "/home/elhajjad/PhD_Dana_NAS_share/elhajjad/S_SG_MLEPL/Off_ScaledGaussian_l=20_phasecorrec_3_n_49_window_size=7/toSAR/hdr_img/" \
#     --output_path "/home/elhajjad/PhD_Dana_NAS_share/elhajjad/S_SG_MLEPL/Off_ScaledGaussian_l=20_phasecorrec_3_n_49_window_size=7/" \
#         --n_images 20 --name_approach "Off_ScaledGaussian_l=20_phasecorrec_3_n_49_window_size=7_date_"
