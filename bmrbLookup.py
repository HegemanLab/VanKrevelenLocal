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


# Takes an individual mass and uses the lookupTable and tolerance ot find the formula for a molecule of that mass
def getFormulaFromMass(mass, lookupTable, tolerance=.005):

    # get list of weights to make checking tolerance window easier
    wt_list = list(lookupTable["Formula_mono_iso_wt_nat"])

    # Check all weights to see which fit in the tolerance window
    bools = [True if (mass + tolerance) >= x >= (mass - tolerance) else False for x in wt_list]

    # get the formulas of the molecules with masses that were within the tolerance
    returned = lookupTable[bools]['Formula']

    # Set up in case nothing was found
    comp = "No Match"
    try:
        # remove duplicate values that are returned
        comp = set(returned)

        # If anything was found within the tolerance
        if len(comp) > 0:

            # make a copy so that comp can still be returned either way
            compCopy = copy.copy(comp)
            compsTemp = []

            # loop through each item in the set
            for i in range(0, len(comp)):

                # remove whitespace because of how extractNeededElementalData is written
                spaced = compCopy.pop()
                compsTemp.append(spaced.replace(" ", ""))

            # set up comp for returning the right values
            comp = compsTemp

    # return the compound formula
    finally:
        return comp

# adjust for 'pos' or 'neg' polarity scans
def adjust(mass, polarity):

    # value to adjust by
    hm = 1.007276

    if polarity == 'pos':
        mass += hm
    elif polarity == 'neg':
        mass -= hm

    return mass


