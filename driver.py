'''
This script takes in an mzXML file and outputs the masses of all peaks into two .txt files.
Note, this code is configured for MS that output MS levels as either 0 (positive mode) 
or 1 (negative mode). If your MS is set up differently you will need to make edits to this code
'''
import sys
import os
import webbrowser

# additional created classes/packages
from MzXML import MzXML
from writeTxt import writeTxt
from process_mzs import process_mzs


# Message in case of error
usage_mesg = 'driver.py <mzXML file>'

# Checks to make sure two and only two arguments were entered into the command line
if len(sys.argv) != 2:
    print usage_mesg
    sys.exit(1)

# Gets the filename from the second argument passed in and makes sure the file can be found
filename_mzXML = sys.argv[1]
if not os.access(filename_mzXML, os.R_OK):
    print "%s is not accessible." % filename_mzXML
    print usage_mesg
    sys.exit(1)

# Creates an MzXML object from the file provided
mzXML = MzXML()
mzXML.parse_file(filename_mzXML)

# Takes in the mzXML object and processes all the data to extract a list with both the positive and
# negative mz values extracted. Then writes those to two .txt files.
neg_pos_mz_sets = process_mzs(mzXML)
if neg_pos_mz_sets[0]:
    writeTxt(neg_pos_mz_sets[0], filename_mzXML, 0)
if neg_pos_mz_sets[1]:
    writeTxt(neg_pos_mz_sets[1], filename_mzXML, 1)


# Automatically opens the web browser with the calculator page open
# webbrowser.open('http://www.bmrb.wisc.edu/metabolomics/mass_query.php', new=1)

print('done')
