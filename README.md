# TTW Artifacts

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/TTW-Artifacts/master)

This repository describes all the public artifacts related to the Time-Triggered Wireless Architecture project, presented in the following paper:

> **Time-Triggered Wireless Architecture**  
Romain Jacob, Licong Zhang, Marco Zimmerling, Samarjit Chakraborty, Lothar Thiele   
Accepted to ECRTS 2020  
[arXiv (submitted version)](https://arxiv.org/abs/2002.07491)

We use the sections of this paper as reference in the rest of this file.

<!-- TOC depthFrom:2 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Reproducing the data processing](#reproducing-the-data-processing)
- [TTnet model](#ttnet-model)
- [Reproducing the plots](#reproducing-the-plots)
- [Compile and run TTnet](#compile-and-run-ttnet)
- [Run the TTW scheduler](#run-the-ttw-scheduler)
- [Other Related Resources](#other-related-resources)

<!-- /TOC -->

<!-- ############################################### -->
## Compile and run TTnet
<!-- ############################################### -->

Our TTnet implementation (Section 3.2) is based on [Baloo](https://github.com/ETHZ-TEC/Baloo/tree/master), a design framework for network stacks based on Synchronous Transmissions. Instructions for setting up and running Baloo are described in details in the [Baloo Wiki](https://github.com/ETHZ-TEC/Baloo/wiki).

The TTnet implementation is located under `examples/baloo-ttnet`. This directory includes a README file that details the build and run commands, as well as information related to the TTnet implementation, how to configure it, and how to use it.

<!-- ############################################### -->
## TTnet model
<!-- ############################################### -->

This repository contains all the information required to use the TTnet time and energy model (Section 3.3). This requires
+ The `/src` directory, which includes the Python source code
+ The Python modules listed in the `requirements.txt` file

The `ttnet_model.ipynb` notebook presents the model, illustrates the various functions computing the model equations, and shows some sample plots comparing the effects of different parameter values.  
This notebook can be run directly in your web browser [using Binder](https://mybinder.org/) (it may take a few minutes to launch).

> [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/TTW-Artifacts/master) and open the `ttnet_model.ipynb` notebook; or use this
[direct link.](https://mybinder.org/v2/gh/romain-jacob/TTW-Artifacts/master?filepath=.%2Fttnet_model.ipynb)

<!-- ############################################### -->
## Run the TTW scheduler
<!-- ############################################### -->

Our implementation of the TTW Scheduler (Section 4) is located in its own GitHub repository:
+ [GitHub repo: romain-jacob/TTW-Scheduler][ttw_repo]
+ [Zenodo archive: ![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3530665.svg)][ttw_zenodo]

The scheduler is implemented in [Matlab][1] and uses [Gurobi][2] to solve the MILP formulation. The [TTW Scheduler repository][ttw_repo] contains detailed information allowing to
+ Setup Matlab and Gurobi
+ Formulate a scheduling problem (eg, how to specify applications, modes, etc.)
+ Reproduce the evaluation of TTW minimal inheritance approach (Section 5.2)

> Although Matlab and Gurobi are both commercial software (which is not ideal), free academic and/or student licenses are currently available from the software vendors.

[1]: https://www.mathworks.com/products/matlab.html
[2]: https://www.gurobi.com/
[ttw_repo]: https://github.com/romain-jacob/TTW-Scheduler
[ttw_zenodo]: https://doi.org/10.5281/zenodo.3530665

<!-- Link and instruction to run the TTW Scheduler (Matlab (with versions) + Gurobi). Check what has been written for the thesis already (I did stuff for DRP, don't remember for TTW) -->


<!-- ############################################### -->
## Reproducing the data processing
<!-- ############################################### -->

This repository contains all the information required to re-run the data processing for the TTnet validation experiments (Section 5.1). This requires
+ The `/src` directory, which includes the Python source code
+ The Python modules listed in the `requirements.txt` file
+ The raw data raw data from the FlockLab experiments (one .zip of ~70Mb), which is available [on Zenodo](https://doi.org/10.5281/zenodo.3530721) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3530721.svg)](https://doi.org/10.5281/zenodo.3530721)

The `ttnet_model_validation.ipynb` notebook summarizes the whole procedure, describes the steps required to do the processing, download the raw data, and produces some visualizations of the processed data.  
This notebook can be run directly in your web browser [using Binder](https://mybinder.org/) (it may take a few minutes to launch).

> [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/TTW-Artifacts/master) and open the `ttnet_model_validation.ipynb` notebook; or use this
[direct link.](https://mybinder.org/v2/gh/romain-jacob/TTW-Artifacts/master?filepath=.%2Fttnet-model-validation.ipynb)


<!-- ############################################### -->
## Reproducing the plots
<!-- ############################################### -->

This repository contains all the information required to reproduce all the plots presented in the paper. This requires
+ The `/src` directory, which includes the Python source code
+ The Python modules listed in the `requirements.txt` file
+ The processed data, located in the `/data_processed` directory. Alternatively, you may re-run the processing from the raw data (see [Reproducing the data processing](#reproducing-the-data-processing)).

The `ttw_plots.ipynb` notebook produces, displays, and (optionally) saves all plots presented in the paper.  
This notebook can be run directly in your web browser [using Binder](https://mybinder.org/) (it may take a few minutes to launch).

> [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/TTW-Artifacts/master) and open the `ttw_plots.ipynb` notebook; or use this
[direct link.](https://mybinder.org/v2/gh/romain-jacob/TTW-Artifacts/master?filepath=.%2Fttw_plots.ipynb)


<!-- ############################################### -->
## Other related resources
<!-- ############################################### -->
+ TTW poster
+ Previous paper (DATE)
+ Thesis chapter
