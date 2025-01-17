# -----------------------------------------------------------------
# Libraries
# -----------------------------------------------------------------

import argparse
import numpy as np

from imagesutils import (save_float, 
                         writehdrfile,
                         coherence_normalization)

# -----------------------------------------------------------------
# Function to parse command-line arguments
# -----------------------------------------------------------------

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Process SAR phase and coherence data.")
    
    # Add required arguments
    parser.add_argument('--name_approach', type=str, required=True, help="Prefix for the output filenames.")
    parser.add_argument('--phases_file', type=str, required=True, help="Path to the phase file (3D numpy array).")
    parser.add_argument('--coherence_file', type=str, required=True, help="Path to the coherence file (4D numpy array).")
    parser.add_argument('--output_path', type=str, required=True, help="Directory where the results will be saved.")
    
    # Parse and return the arguments
    return parser.parse_args()


# -----------------------------------------------------------------
# Main processing function
# -----------------------------------------------------------------

def main(args):
    """Main processing function."""
    # User parameters
    name_approach = args.name_approach  # e.g., "S_SG_MLE_PL_date_"
    phases_file = args.phases_file
    coherence_file = args.coherence_file
    output_path = args.output_path

    # Load the phase file
    phases = np.load(phases_file)  # 3D array

    # Load the coherence file
    Sigma = np.load(coherence_file)  # Shape: (shape[0], shape[1], n_images, n_images)

    print('shape : ', phases.shape)

    # Path to save the results
    path = output_path

    # Number of images
    n_images = phases.shape[-1]

    # Shape of a single interferogram
    shape = (phases.shape[0], phases.shape[1])

    # Initialize the coherence matrix
    Sigma_norm = np.zeros((shape[0], shape[1], n_images, n_images))

    # Normalize the coherence matrix for each pixel
    for i in range(shape[0]):
        for j in range(shape[1]):
            Sigma_norm[i, j, :, :] = coherence_normalization(Sigma[i, j, :, :])

    # Process phases and coherences for each image
    for i in range(n_images): 
        # Phase processing
        estimated_inter = phases[:, :, i] 
        filename = path + name_approach + str(i + 1) + "_phase.hdr"
        bandname = name_approach + str(i + 1) + "_phase"
        writehdrfile(phases.shape[0], phases.shape[1], bandname, filename, "phase")
        name_img = path + bandname + ".img"
        save_float(name_img, shape, estimated_inter)

        # Coherence processing
        estimated_coh = Sigma_norm[:, :, 0, i] 
        filename = path + name_approach + str(i + 1) + "_coherence.hdr"
        bandname = name_approach + str(i + 1) + "_coherence"
        writehdrfile(Sigma_norm.shape[0], Sigma_norm.shape[1], bandname, filename, "coherence")
        name_img = path + bandname + ".img"
        save_float(name_img, shape, estimated_coh)


# -----------------------------------------------------------------
# Entry point of the script
# -----------------------------------------------------------------

if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()

    # Call the main function with the parsed arguments
    main(args)
