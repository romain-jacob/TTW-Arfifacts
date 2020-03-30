# TTW Artifacts

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/TTW-Artifacts/master)

This repository describes all the public artifacts related to the Time-Triggered Wireless Architecture project, presented in the following paper:

> **Time-Triggered Wireless Architecture**  
Romain Jacob, Licong Zhang, Marco Zimmerling, Samarjit Chakraborty, Lothar Thiele   
Accepted to ECRTS 2020  
[arXiv (submitted version)](https://arxiv.org/abs/2002.07491)

<!-- TOC depthFrom:2 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Reproducing the data processing](#reproducing-the-data-processing)
- [TTnet model](#ttnet-model)
- [Reproducing the plots](#reproducing-the-plots)
- [Compile and run TTnet](#compile-and-run-ttnet)
- [Run the TTW scheduler](#run-the-ttw-scheduler)
- [Other Related Resources](#other-related-resources)

<!-- /TOC -->



## Reproducing the data processing

This repository contains all the information required to re-run the data processing for the TTnet validatation experiments (Section 5.1). This requires
+ The `/src` directory, which includes the Python source code
+ The Python modules listed in the `requirements.txt` file
+ The raw data raw data from the FlockLab experiments (one .zip of ~70Mb), which is available [on Zenodo](https://doi.org/10.5281/zenodo.3530721) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3530721.svg)](https://doi.org/10.5281/zenodo.3530721)

The `ttnet_model_validation.ipynb` notebook summarizes the whole procedure, describes the steps required to do the processing, download the raw data, and produces some visualizations of the processed data.  
This notebook can be run directly in your web browser [using Binder](https://mybinder.org/) (it may take a few minutes to launch).

[Direct link : ![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/TTW-Artifacts/master?filepath=.%2Fttnet-model-validation.ipynb)

## TTnet model

See `ttnet_model.ipynb`. Can be run [in Binder.](https://mybinder.org/v2/gh/romain-jacob/TTW-Arfifacts/master)  
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/TTW-Arfifacts/master)


## Reproducing the plots
See `ttnet_plots.ipynb`. Can be run [in Binder.](https://mybinder.org/v2/gh/romain-jacob/TTW-Arfifacts/master)  
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/TTW-Arfifacts/master)

## Compile and run TTnet
Link and instruction to compile the TTnet implementation in Baloo. Ideally, this would include a way to generate and run a FlockLab test (but needs adaptations due to the transition to FlockLab2)

## Run the TTW scheduler
Link and instruction to run the TTW Scheduler (Matlab (with versions) + Gurobi). Check what has been written for the thesis already (I did stuff for DRP, don't remember for TTW)

## Other Related Resources
+ TTW poster
+ Previous paper (DATE)
+ Thesis chapter
