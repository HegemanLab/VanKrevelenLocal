import pandas as pd


# import csv as DataFrame
def getLookupTable(tableFilename):
    lookup_df = pd.read_csv(tableFilename)
    return lookup_df


# "Formula_mono_iso_wt_nat"
def getFormulaFromMass(mass, lookupTable, tolerance=.005):

    wt_list = list(lookupTable["Formula_mono_iso_wt_nat"])

    bools = [True if (mass + tolerance) > x > (mass - tolerance) else False for x in wt_list]

    returned = lookupTable[bools]['Formula']

    comp = "No Match"
    try:
        # get just the first formula. They all should be the same b/c the mass is the same, right?
        comp = set(returned)

        for i in range(0, len(comp)):
            # remove whitespace because of how extractNeededElementalData is written
            comp[i] = comp[i].replace(" ", "")

    # return the compound formula
    finally:
        return comp

# adjust for 'pos' or 'neg' polarity scans
def adjust(mass, polarity):

    # Not sure which of these would be best. regular H+ or monoisotopic H+
    hm = 1.007276

    if polarity == 'pos':
        mass += hm
    elif polarity == 'neg':
        mass -= hm

    return mass


