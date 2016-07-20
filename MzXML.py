'''
Class for dealing with mzXML files and handling the data. Particularly useful for decoding the
peak lists.  Found from: https://code.google.com/p/massspec-toolbox/source/browse/#svn/trunk/mzxml
and minimal updates made.
'''
import sys
import base64  # Imports a binary converter package
import struct
import gzip  # For file handling
import xml.parsers.expat
from MSScan import MS1Scan, MS2Scan


# Defines a class of objects of MzXML type. Will initialize with the following values.
class MzXML():
    def __init__(self):
        self.msLevel = 0
        self.current_tag = ''
        self.tag_level = 0
        self.MS1_list = []
        self.MS2_list = []

    '''
    Function that decodes a single line. ***NOTE*** This is where files being run through a different
    mzXML converter broke down. MM_File_Conversion3 was used in testing to convert .raw files (not folders)
    to mzXML files. If this converter is used, this code should work but currently looking into ways to
    make this work with other, more broadly used converters. mzML is another file format that should work
    more consistently if this gives you issues.
    '''

    def decode_spectrum(self, line):
        decoded = base64.decodestring(line)

        # Determines unpack format which is specific to the type of data being examined
        tmp_size = len(decoded) / 4
        unpack_format1 = ">%dL" % tmp_size

        idx = 0

        # Declares list for mzs and intensities
        mz_list = []
        intensity_list = []

        # Loops through the decoded, unpacked line and breaks them apart into mz and intensity lists
        for tmp in struct.unpack(unpack_format1, decoded):
            tmp_i = struct.pack("I", tmp)
            tmp_f = struct.unpack("f", tmp_i)[0]
            if (idx % 2 == 0):
                mz_list.append(float(tmp_f))
            else:
                intensity_list.append(float(tmp_f))
            idx += 1

        # Returns the lists of intensities and mzs
        return mz_list, intensity_list

    def _start_element(self, name, attrs):
        # Increments the tag_level for the MzXML object and updates the current_tag
        self.tag_level += 1
        self.current_tag = name

        # If it's a precursorMz it adjusts accordingly
        if name == 'precursorMz':
            self.MS2_list[-1].precursor_intensity = float(attrs['precursorIntensity'])

            self.MS2_list[-1].precursor_charge = 0
            if attrs.has_key('precursorCharge'):
                self.MS2_list[-1].precursor_charge = int(attrs['precursorCharge'])
        # If the element being read in is a scan, checks what the scan level is and initializes a list of that type
        if name == 'scan':
            self.msLevel = int(attrs['msLevel'])
            if self.msLevel == 1:
                tmp_ms = MS1Scan()
                '''
                Note, the below and above code is critical and will need to be adjusted depending on how your machine
                does scans. This setting will impact numerous other factors so it is critical to get this right.
                This same change needs to be made on line 96 as called out in the other comment.
                The main thing to be aware of is that msLevel == 1 is used for negative scans and msLevel == 0
                is used for positive mode scans which may vary by machine. Positive and negative modes are also
                handled by double checking polarity but if your machine uses something other than msLevel 0 or 1
                this will still need to be changed.
                '''
            elif (self.msLevel == 0):
                tmp_ms = MS2Scan()

            else:
                print("What is it?", attrs)
                sys.exit(1)

            # Assigns attributes to their logical properties
            tmp_ms.id = int(attrs['num'])
            tmp_ms.peak_count = int(attrs['peaksCount'])
            # TODO uncomment this section
            # tmp_ms.filter_line = attrs['filterLine']
            tmp_ms.retention_time = float(attrs['retentionTime'].strip('PTS'))
            tmp_ms.low_mz = float(attrs['lowMz'])
            tmp_ms.high_mz = float(attrs['highMz'])
            tmp_ms.base_peak_mz = float(attrs['basePeakMz'])
            tmp_ms.base_peak_intensity = float(attrs['basePeakIntensity'])
            tmp_ms.total_ion_current = float(attrs['totIonCurrent'])
            tmp_ms.list_size = 0
            tmp_ms.encoded_mz = ''
            tmp_ms.encoded_intensity = ''
            tmp_ms.mz_list = []
            tmp_ms.intensity_list = []
            tmp_ms.polarity = attrs['polarity']

            # Adds the scan to the correct list of scans
            if self.msLevel == 1:
                self.MS1_list.append(tmp_ms)
            elif self.msLevel == 0:  # *************** changed ms level from == 2 to ==0**************
                self.MS2_list.append(tmp_ms)

    # Reduces the tag level, sets current_tag to '' and msLevel at 0
    def _end_element(self, name):
        self.tag_level -= 1
        self.current_tag = ''
        self.msLevel == 0

    def _char_data(self, data):
        # if self.current_tag == 'precursorMz':
        #     self.MS2_list[-1].precursor_mz = float(data)

        if self.current_tag == 'peaks':
            mz_list, intensity_list = self.decode_spectrum(data)
            mz_string = ''.join([struct.pack('>f', i) for i in mz_list])
            intensity_string = ''.join([struct.pack('>f', i) for i in intensity_list])
            if self.msLevel == 1:
                self.MS1_list[-1].list_size += len(mz_list)
                self.MS1_list[-1].encoded_mz += base64.encodestring(mz_string)
                self.MS1_list[-1].encoded_intensity += base64.encodestring(intensity_string)
                self.MS1_list[-1].mz_list += mz_list
                self.MS1_list[-1].intensity_list += intensity_list

            elif self.msLevel == 0:
                self.MS2_list[-1].list_size += len(mz_list)
                self.MS2_list[-1].encoded_mz += base64.encodestring(mz_string)
                self.MS2_list[-1].encoded_intensity += base64.encodestring(intensity_string)
                self.MS2_list[-1].mz_list = mz_list
                self.MS2_list[-1].intensity_list = intensity_list

    def parse_file(self, filename_xml):
        sys.stderr.write("Reading %s ... " % filename_xml)
        f_xml = open(filename_xml, 'r')
        if filename_xml.endswith('.gz'):
            f_xml = gzip.open(filename_xml, 'rb')
        content_list = []
        for line in f_xml:
            content_list.append(line)
        f_xml.close()

        expat = xml.parsers.expat.ParserCreate()
        expat.StartElementHandler = self._start_element
        expat.EndElementHandler = self._end_element
        expat.CharacterDataHandler = self._char_data
        expat.Parse("".join(content_list))

        sys.stderr.write("Done\n")
