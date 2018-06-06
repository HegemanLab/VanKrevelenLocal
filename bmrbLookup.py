'''
This script uses pandas data frames to look up the formulas for the input masses
based on the BMRB compound database which can be found at:
http://www.bmrb.wisc.edu/ftp/pub/bmrb/relational_tables/metabolomics/Chem_comp.csv
'''

import pandas as pd
import copy

# import csv as DataFrame
def getLookupTable(tableFilename):
    lookup_df = pd.read_csv(tableFilename)
    return lookup_df


# Takes an individual mass and uses the lookupTable and tolerance to find the formula for a molecule of that mass
# tolerance is given in ppm
def getFormulaFromMass(mass, lookupTable, tolerance=5):

    # get list of weights to make checking tolerance window easier
    wt_list = list(lookupTable["Formula_mono_iso_wt_nat"])

    # Check all weights to see which fit in the tolerance window
    # bools = [True if (mass + tolerance) > x > (mass - tolerance) else False for x in wt_list]

    # other ppm check
    bools = [True if (abs(mass - x) / x) * 1000000 <= tolerance else False for x in wt_list]

    # get the formulas of the molecules with masses that were within the tolerance
    returned = lookupTable[bools][['Formula_mono_iso_wt_nat', 'Formula']]
    returned['diff'] = abs(returned['Formula_mono_iso_wt_nat'] - mass)

    # Set up in case nothing was found
    comp = "No Match"
    try:
        # If there were multiple matches, this returns the 'best' match based on it being closest in mass
        comp = returned['Formula'][returned['diff'].idxmin()]

    # return the compound formula
    finally:
        return comp

# adjust for 'pos' or 'neg' polarity scans
def adjust(mass, polarity):

    # value to adjust by
    hm = 1.007276

    if polarity == 'pos':
        mass -= hm
    elif polarity == 'neg':
        mass += hm

    return mass


