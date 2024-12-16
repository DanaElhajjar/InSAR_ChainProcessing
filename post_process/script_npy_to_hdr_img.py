# -----------------------------------------------------------------
# Librairies
# -----------------------------------------------------------------

import numpy as np

from imagesutils import (save_float, 
                         writehdrfile,
                         coherence_normalization)

if __name__ == "__main__":

    name_approach = "" # example : "S_SG_MLE_PL_date_"

    # load phase file
    phases = np.load("") # 3d

    # load coherence file
    Sigma = np.load("") # shape : (shape[0], shape[1], n_images, n_images)

    print('shape : ', phases.shape)

    # path to save the results
    path = ""

    # number of images
    n_images = phases.shape[-1]

    # shape of one interferogram
    shape = (phases.shape[0], phases.shape[1])

    # initialmization for the coherence matrix
    Sigma_norm = np.zeros((shape[0], shape[1], n_images, n_images))

    for i in range(shape[0]):
        for j in range(shape[1]):
            Sigma_norm[i, j, :, :] = coherence_normalization(Sigma[i, j, :, :])

    for i in range(n_images): 
        # phase processing
        estimated_inter = phases[:, :, i] 
        filename = path+name_approach+str(i+1)+"_phase.hdr"
        bandname  = name_approach+str(i+1)+"_phase"
        writehdrfile(phases.shape[0], phases.shape[1], bandname, filename,"phase")
        name_img = path+bandname+".img"
        save_float(name_img, shape, estimated_inter)

        # coherence processing
        estimated_coh = Sigma_norm[:, :, 0, i] 
        filename = path+name_approach+str(i+1)+"_coherence.hdr"
        bandname  = name_approach+str(i+1)+"_coherence"
        writehdrfile(Sigma_norm.shape[0], Sigma_norm.shape[1], bandname, filename,"coherence")
        name_img = path+bandname+".img"
        save_float(name_img, shape, estimated_coh)

    