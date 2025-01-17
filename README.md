# InSAR Chain Processing

This repository is dedicated to the processing workflow for time series of SAR images.  This workflow enables the conversionof a time series of SAR images into a time series of interferograms. It consists of two main stages:  Pre-processing and Post-processing.  The Pre-processing stage involves transforming SAR images into interferograms,  while thePost-processing stage focuses on converting the outputs of our algorithms (in .npy format) into SAR-compatible formats, phase unwrapping, and estimating the time series of displacements.

# Code organisation

├── environment.yml <br>
├── __init__.py <br>
├──pre_process <br>
│   ├── GenerateInterf.py <br>
│   ├── processing_chain_topo_phase_removal.xml <br>
│   └── utils.py <br>
└── post_process <br>
    ├── displacement_map.xml <br>
    ├── imagesutils.py <br>
    ├── script_displacement_map.py <br>
    ├── script_npy_to_hdr_img.py <br>
    ├── script_snaphu_export.py <br>
    ├── script_unwrap_terminal.py <br>
    └── snaphu_export.xml <br>


## Pre-processing 
The pre-processing phase involves executing the GenerateInterf.py Python script. This script takes the path to the raw SAR images as input and performs the following tasks:

- Coregisters the images (relative to the first date).
- Generates interferograms relative to the first date, which will serve as the "Master" image.

```bash
python GenerateInterf.py --pathInput <path_to_raw_SAR_images> \
                        --pathOutput_interferograms <path_to_output_interferograms> \
                        --pathOutput_coregistered <path_to_output_coregistered_images> \
                        --pathSNAPGraph <path_to_snap_graph> \
                        --pathGPT <path_to_gpt_executable> \
                        --swath <swath_number> \
                        --delay <delay_in_days>
```
## Post-processing 

The post-processing phase consists of three main steps: converting phase estimates, performing phase unwrapping and displacement time series estimation.

### Step 1: Convert Phase Estimates
The first step is to convert the phase estimates stored in .npy files into a format compatible with the SNAP software. This is achieved using the script_npy_to_hdr_img.py script.

```bash
python script_npy_to_hdr_img.py --name_approach <name_of_the_approach_date> \
                                --phases_file <path_to_the_estimated_phases> \
                                --coherence_file  <path_to_the_estimated_coherences>\
                                --output_path <path_to_save_output>
```

### Step 2: Phase Unwrapping

After converting the phase estimates, phase unwrapping is performed. This is done in two sub-steps:

- Run script_snaphu_export.py to generate the configuration file.
- Run script_unwrap_terminal.py to perform phase unwrapping using the generated configuration file.

```bash
python script_snaphu_export.py --pathInput <path_to_images> \
                               --pathOutput_unwrapped_interferograms <output_path_to_unwrapped_interferograms> \
                               --pathSNAPGraph <path_to_SNAP_graph> \
                               --pathGPT <path_to_GPT> \
                               --name_approach <approach_name>

python script_unwrap_terminal.py --father_folder <pathto_unwrapped_interferograms> \
                                 --conf_file "snaphu.conf" \
                                 --comment_word "LOGFILE"
```

### Step 3: Displacement estimation
The final step involves estimating the displacements from the unwrapped phase data. This is done using the script_displacement_map.py script, which generates a time series of displacement values.

```bash
python script_displacement_map.py --pathInput1 <path_to_wrapped_interferograms \
                                  --pathInput2 <path_to_unwrapped_interferograms> \
                                  --pathOutput_displacement <output_path_to_dispalcement> \
                                  --pathSNAPGraph <path_to_SNAP_graph> \
                                  --pathGPT <path_to_GPT> \
                                  --name_approach <name_approach>
```

## Environment

A conda environment is provided in the file `environment.yml` To create and use it run:

```console
conda env create -f environment.yml
conda activate insar_processing_chain
```

### Authors

* Dana El Hajjar, mail: dana.el-hajjar@univ-smb.fr, dana.el-hajjar@centralesupelec.fr

Copyright @Université Savoie Mont Blanc, 2025