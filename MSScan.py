'''
Helper class for dealing with mzXML files and handling the data. Particularly useful for decoding the
peak lists.  Found from: https://code.google.com/p/massspec-toolbox/source/browse/#svn/trunk/mzxml
and minimal updates made.
'''

# Class for a single MS scan, not the complete set of scans.
class MSScan:
    def __init__(self):
        self.id = 0
        self.peak_count = 0
        self.filter_line = ''
        self.retention_time = 0.0
        self.low_mz = 0.0
        self.high_mz = 0.0
        self.base_peak_mz = 0.0
        self.base_peak_intensity = 0.0
        self.total_ion_current = 0.0
        self.list_size = 0
        self.encoded_mz = ''
        self.encoded_intensity = ''
        self.mz_list = []
        self.intensity_list = []


# Used as negative scan lists
class MS1Scan(MSScan):
    def __init__(self):
        pass


# Used as positive scan lists
class MS2Scan(MSScan):
    def __init__(self):
        pass
        self.ms1_id = 0
        self.precursor_mz = 0.0
        self.precursor_intensity = 0.0
        self.precursorCharge = 0
