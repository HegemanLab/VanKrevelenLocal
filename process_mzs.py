'''
Churns through an mzXML object to generate lists of positive and negative
mz values.
'''


# Takes an mzXML object which contains a list of intensities, a
# list of mzs, and a value for the threshold intensity for filtering.
def process_mzs(mzXML_obj, threshold=.1):  # What fraction of the max intensity you want to use for a threshold
    # For elements that clear the filter
    keepers_neg_mz = []
    keepers_pos_mz = []

    # Loops through positive list and negative list and adds mz values to the keeper list when the intensity is
    # above a threshold
    for scan in mzXML_obj.MS1_list:
        thresh = max(scan.intensity_list) * threshold
        i = 0
        for peak in scan.intensity_list:
            if peak > thresh:
                if scan.polarity == '-':
                    keepers_neg_mz.append(scan.mz_list[i])
                elif scan.polarity == '+':
                    keepers_pos_mz.append(scan.mz_list[i])
            i += 1
    for scan in mzXML_obj.MS2_list:
        thresh = max(scan.intensity_list) * threshold
        i = 0
        for peak in scan.intensity_list:
            if peak > thresh:
                if scan.polarity == '-':
                    keepers_neg_mz.append(scan.mz_list[i])
                elif scan.polarity == '+':
                    keepers_pos_mz.append(scan.mz_list[i])
            i += 1

    # Removes duplicates
    filtered_neg_mz = list(set(keepers_neg_mz))
    filtered_pos_mz = list(set(keepers_pos_mz))

    # Combines list where negatives are in the 0 position and positives in the 1
    combo_list = [filtered_neg_mz, filtered_pos_mz]
    return combo_list
