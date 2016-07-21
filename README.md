# VanKrevlenCommandLine

## Introduction and General Notes
Code developed by the Hegeman Lab for Van Krevelen analysis of mass spec data. The Hegeman Lab (The Plant Metabolomics Lab at the University of Minnesota) applies mass spectrometry-based metabolomics to plant biological or agricultural questions while simultaneously trying to improve current metabolomics methodologies. In particular we are interested in way that stable isotopes and mass spectrometry can be used for methodological innovations in metabolomics and the analysis of metabolic flux.

If you use this tool or any others associated with the Hegeman Lab we ask that you please reference us in your projects.

Further, if you are looking to contribute to this code base please make sure to follow the conventions used through out the existing code and also please be thorough in commenting your code. This script is intended to be user friendly, particularly to non-programmers as many individuals who will want to use this tool will have little to no background in programming. For this reason some efficiency was compromised for simplicity in the creation of this script. If your contributions lead to any changes in how the program is used, then also update the instructions.

Some notes about the technology specifications of this script: 	

* Uses Python 2.7 - unsure of compatibility with 3.5, but incompatible with 3.4

* All packages used can be obtained through downloading this package and the Anaconda Python Distribution from Continuum Analytics (it's free, don't worry :) ).

* Depending on how your computer is configured, you may be able to run the scripts by using the same commands listed below but with out the leading word "python".

## Usage
To run this program, save a copy of your mzXML file to this folder (or the same folder where the script is located). Open the command prompt and navigate into this folder. 

The commands should be something similar to...
> \>cd Desktop	
> \>cd VanKrevelenLocal	

...if you saved the script to your desktop. If you need to move up a file level, use the "cd .." command.
A decent introduction to the commandline can be found [here](http://lifehacker.com/5633909/who-needs-a-mouse-learn-to-use-the-command-line-for-almost-anything), but this has way more information than you will need for running this script.
	
Note: if running on OSX these commands are case sensitive

Once setup is complete and you have navigated to the folder in the command line enter:

> \>python aggregateDriver.py

To launch into the program. From here you will be guided step by step through the command prompt. The first time you run the script you will need to use the 'new' mode rather than the 'load' mode unless you have access to an output .txt file from a previous session.

## Files
A brief description of some of the files in this repo and their roles. 

#### aggregateDriver.py
The workhorse of this set of scripts. Provides a command line tool for running various versions of the Van Krevelen diagram analysis. This script is useful for looking at a few different types of analysis but if you want to do large scale analysis this script can also be used as a jumping off point to see how the pieces fit together before building your own more automated version. 

#### bmrb-db.csv and bmrbLookup.py
bmrb-db.csv is a local file that effectively holds all of the information used by [Find Formula by Mass](http://bmrb.wisc.edu/metabolomics/mass_query.php) tool from the Biological Magnetic Resonance Data Bank (BMRB) run out of the University of Wisconsin. mbrbLookup.py is  a script that contains a couple simple functions for looking through the csv to try to immitate the functionality of the formula finder while doing it all locally to increase speed and allow for the script to run indepenednet of an internet connection. 

#### VanKrevelen(type of map).py
Each of these scripts contain functions for generating the designated types of plots. This may be useful if you want to write your own script using some functions from here. Each of the VanKrevelen functions takes data that has been passed from process_mzs or process_mzs_mzML to bmrbLookup to extractNeededElementalData to processElementalData and this workflow can also be utilized in custom applications. 

## Acknowledgements
* Bald, T., Barth, J., Niehues, A., Specht, M., Hippler, M., and Fufezan, C. (2012) pymzML - Python module for high throughput bioinformatics on mass spectrometry data, Bioinformatics, doi: 10.1093/bioinformatics/bts066
* Heatmap from http://jjguy.com/heatmap/
* mzXML handler from https://code.google.com/p/massspec-toolbox/source/browse/#svn/trunk/mzxml
* "BioMagResBank", Eldon L. Ulrich; Hideo Akutsu; Jurgen F. Doreleijers; Yoko Harano; Yannis E. Ioannidis; Jundong Lin; Miron Livny; Steve Mading; Dimitri Maziuk; Zachary Miller; Eiichi Nakatani; Christopher F. Schulte; David E. Tolmie; R. Kent Wenger; Hongyang Yao; John L. Markley; Nucleic Acids Research 36, D402-D408 (2008) doi: 10.1093/nar/gkm957 


## Hegeman Lab - University of Minnesota Twin-Cities
This code was developed for use in the Hegeman Lab at the University of Minnesota Twin-Cities. If you use this script in your research, please don't forget to site us. Additionally, if there are any questions about how to use this code, feel free to contact the lab or the scripts creater directly through GitHub. 

