'''
Similar to the first driver class but handles mzML files, not mzXML files.
'''

import sys
import os
import webbrowser


# additional created classes/packages
from writeTxt import writeTxt

from process_mzs_mzML import process_mzs

# Message in case of error
usage_mesg = 'driverML.py <mzML file>'

# Checks to make sure two and only two arguments were entered into the command line
if len(sys.argv) != 2:
    print usage_mesg
    sys.exit(1)

# Gets the filename from the second argument passed in and makes sure the file can be found
filename = sys.argv[1]
if not os.access(filename, os.R_OK):
    print "%s is not accessible." % filename
    print usage_mesg
    sys.exit(1)

sys.stderr.write("Reading %s ... " % filename)

# Takes in the mzML file and processes all the data to extract a list with both the positive and
# negative mz values extracted. Then writes those to two .txt files.
neg_pos_mz_sets = process_mzs(filename)

if neg_pos_mz_sets[0]:
    writeTxt(neg_pos_mz_sets[0], filename, 0)
if neg_pos_mz_sets[1]:
    writeTxt(neg_pos_mz_sets[1], filename, 1)

# Automatically opens the web browser with the calculator page open
# webbrowser.open('http://www.bmrb.wisc.edu/metabolomics/mass_query.php', new=1)

print('done')
