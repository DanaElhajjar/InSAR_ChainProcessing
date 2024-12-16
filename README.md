# InSAR ChainProcessing

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
