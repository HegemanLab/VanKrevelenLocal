'''
Can run this script to navigate through the entire local workflow. Works for single input files or multiple.
'''

import os
import extractNeededElementalData
import processElementalData
import bmrbLookup as bmrb
from process_mzs_mzML import process_mzs as ML_process
from MzXML import MzXML
from process_mzs import process_mzs as XML_process
from flexPlot import plotVanK

# Begin command line interaction
print("\nWelcome to the Van Krevelen Aggregator.")

# set up flag for loop
new_ratios_flag = False

# loop to ensure good input
while not new_ratios_flag:
    try:
        new_ratios = str(raw_input("\nWould you like to start with new data files (mzXML or mzML) or\n"
                                   "load already generated ratio files?\n"
                                   "\nEnter 'new' to load new data or 'load' to load existing files: "))
        new_ratios = new_ratios.lower()

        # if a good answer is provided, end loop
        if new_ratios == 'new' or new_ratios == 'load':
            new_ratios_flag = True

    except:
        # reprompt if original input causes an error
        new_ratios = raw_input("\nEnter 'new' or 'load': ")
        new_ratios = new_ratios.lower()

        # if a good answer is provided, end loop
        if new_ratios == 'new' or new_ratios == 'load':
            write_ratios_flag = True

# Move into loading new data files
if new_ratios == 'new':

    # Set up variable for the list of file names
    files = []

    # prompt for input
    print("Please enter each file you would like to process one at at time.")
    print("When you are done entering files, type 'done' and remember to include the file extensions (.mzXML or .mzML).\n")
    print("Now enter your first file, then press return."
          "\nRemember to enter file names with extensions.\n")
    new_file = raw_input("File Name: ")

    # Continues to add as many files as the user wants.
    while new_file.lower() != "done":

        # Makes sure file is accessible
        if not os.access(new_file, os.R_OK):
            print "%s is not accessible." % new_file
            print "Please try again. The files you use must be in the same file as this script."

        else:

            # Checks for one of the two desired file extensions and if the file is accessible and has the correct
            # ending then it is added to the list of the files.
            # This isn't a perfect error catching method but should catch enough.
            if ".mzXML" in new_file or ".mzML" in new_file:
                files.append(new_file)

            else:
                print("\nIncorrect file extension.")

        # Re-prompt
        print("\nEnter another file with its extension, or enter 'done' and hit return.")
        new_file = raw_input("\nEnter Input: ")

    # explain what the threshold is
    print("\nNext this script will process your files. \nIt will do so by processing each file individually. \nTo do so "
          "it will look at the maximum intensity of a spectrum in the file and then assign a threshold to value that "
          "is some percentage of that maximum. \nThe threshold will be used to determine what values are significant and "
          "what values are just noise. \nWe recommend a threshold of 10% but you can set your own here. Please enter your "
          "threshold percentage as a number with no percentage sign. \n(For example, if you wanted 15%, enter 15)")

    # get input and set up flag
    threshold_input = raw_input("\nThreshold: ")
    t_flag = False

    # checks to make sure an appropriate threshold is entered
    while not t_flag:
        try:
            threshold = float(threshold_input) * .01
            t_flag = True

        # Catch non numeric values that were entered
        except ValueError or TypeError:
            threshold_input = raw_input("\nIncorrect input, please enter just a number.\nThreshold: ")

    # prepares to process mzs from input files
    neg_pos_mz_sets = [[], []]

    # Use correct processing based on file type. Gets both pos and neg mode because this check is made anyways so little
    # cost to just gather both sets here.
    for f in files:
        if ".mzXML" in f:
            mzXML = MzXML()
            mzXML.parse_file(f)
            neg_pos_mz_sets_temp = XML_process(mzXML, threshold=threshold)
            neg_pos_mz_sets[0] = neg_pos_mz_sets[0] + neg_pos_mz_sets_temp[0]
            neg_pos_mz_sets[1] = neg_pos_mz_sets[1] + neg_pos_mz_sets_temp[1]
        elif ".mzML" in f:
            # Use ML processing
            print "Reading %s ..." % f
            neg_pos_mz_sets_temp = ML_process(f, threshold=threshold)
            neg_pos_mz_sets[0] = neg_pos_mz_sets[0] + neg_pos_mz_sets_temp[0]
            neg_pos_mz_sets[1] = neg_pos_mz_sets[1] + neg_pos_mz_sets_temp[1]

    # Removes all duplicates from both neg and pos lists
    neg_pos_mz_sets[0] = list(set(neg_pos_mz_sets[0]))
    neg_pos_mz_sets[1] = list(set(neg_pos_mz_sets[1]))

    # set up flag for loop
    mode_flag = False

    # loop to ensure good input
    while not mode_flag:
        try:
            mode = str(raw_input("\nWould you like to see positive polarity, negative polarity, or both modes?\n"
                                 "\nEnter 'pos', 'neg' or 'both': "))
            mode = mode.lower()

            # if a good answer is provided, end loop
            if mode == 'pos' or mode == 'neg' or mode == 'both':
                mode_flag = True

        except AttributeError:
            # re-prompt if original input causes an error
            mode = raw_input("\nEnter mode: ")
            mode = mode.lower()

            # if a good answer is provided, end loop
            if mode == 'pos' or mode == 'neg' or mode == 'both':
                mode_flag = True

    # set up flag for loop
    write_ratios_flag = False

    # loop to ensure good input
    while not write_ratios_flag:
        try:
            write_ratios = str(raw_input("\nWould you like to write a text file with the generated ratio data?\nThis will "
                                         "greatly reduce processing time if you want to generate other plots in the future.\n"
                                         "This is highly recommended.\n"
                                         "\nEnter 'y' for yes or 'n' for no: "))
            write_ratios = write_ratios.lower()

            # if a good answer is provided, end loop
            if write_ratios == 'y' or write_ratios == 'n':
                write_ratios_flag = True

        except AttributeError:
            # re-prompt if original input causes an error
            write_ratios = raw_input("\nEnter 'y' or 'n': ")
            write_ratios = write_ratios.lower()

            # if a good answer is provided, end loop
            if write_ratios == 'y' or write_ratios == 'n':
                write_ratios_flag = True

    # get lookup table.
    lt = bmrb.getLookupTable('bmrb-db.csv')

    # set up. elements could be changed but would need to do some editing elsewhere.
    elements = ['C', 'H', 'O', 'N']
    neg_comps = list()
    pos_comps = list()

    # check to see if user wanted to process neg mode scans
    if mode == 'neg' or mode == 'both':
        print '\nProcessing negative scans...'
        for mz in neg_pos_mz_sets[0]:

            # adjust mass and search in lookup table. Store result in list.
            neg_comps.extend(bmrb.getFormulaFromMass(bmrb.adjust(mz, 'neg'), lt))

        # Filter out no matches
        neg_comps = filter(lambda a: a != 'No Match', neg_comps)

        # Get elements from compounds
        neg_elements = extractNeededElementalData.find_elements_values(elements_to_find=elements, compounds=neg_comps)

        # Turn elements into ratios
        neg_ratios = processElementalData.process_elemental_data(neg_elements)

        # check if user had wanted to write an output file
        if write_ratios == 'y':

            # get filename
            neg_filename = raw_input("\nWhat would you like the negative output files to be called?"
                                     "\nEnter filename: ")

            # write file
            with open(neg_filename + '.txt', mode='w') as f:

                # loop over and write each ratio to a file
                for ratio in neg_ratios:
                    f.writelines(str(ratio).strip('[]') + '\n')

            print '\nRatios file successfully generated.\n'

        # Start plot generation
        print '\nYour plots will now be generated.'
        plotType = ''

        # get plot type input
        while plotType != 'done':

            plotType = raw_input("\nEnter 'done' to advance or enter a plot type to generate that plot."
                                 "\nPlot options are 'scatter', 'heatmap', and '3d'.\nEnter input: ")

            try:
                if plotType != 'done':
                    print '\nThis may take a moment to make your negative mode plot.' \
                          '\nBe sure to save your plot then close it to continue.'
                    plotVanK(ratiosList=neg_ratios, typeOfPlot=plotType)


            except IOError:
                if plotType != 'done':
                    print '\nIncorrect input. Please enter a valid input.'

                pass

    if mode == 'pos' or mode == 'both':
        print '\nProcessing positive scans...'
        for mz in neg_pos_mz_sets[1]:
            # adjust mass and search in lookup table. Store result in list.
            pos_comps.extend(bmrb.getFormulaFromMass(bmrb.adjust(mz, 'pos'), lt))

        # Filter out no matches
        pos_comps = filter(lambda a: a != 'No Match', pos_comps)

        # Get elements from compounds
        pos_elements = extractNeededElementalData.find_elements_values(elements_to_find=elements, compounds=pos_comps)

        # Turn elements into ratios
        pos_ratios = processElementalData.process_elemental_data(pos_elements)

        if write_ratios == 'y':

            pos_filename = raw_input("\nWhat would you like the positive output files to be called?\nEnter filename: ")

            # write file
            with open(pos_filename + '.txt', mode='w') as f:
                # loop over and write each ratio to a file
                for ratio in pos_ratios:
                    f.writelines(str(ratio).strip('[]') + '\n')

            print '\nRatios file successfully generated.\n'

        print "\nYour plots will now be generated."
        plotType = ''
        while plotType != 'done':

            plotType = raw_input("\nEnter 'done' to advance or enter a plot type to generate that plot."
                                 "\nPlot options are 'scatter', 'heatmap', and '3d'.\nEnter input: ")

            try:
                if plotType != 'done':
                    print '\nThis may take a moment to make your positive mode plot.' \
                          '\nBe sure to save your plot then close it to continue.'
                    plotVanK(ratiosList=pos_ratios, typeOfPlot=plotType)

            except IOError:
                if plotType != 'done':
                    print '\nIncorrect input. Please enter a valid input.'
                pass

# if loading in from text files, read in the ratios, plot it
elif new_ratios == 'load':

    load_flag = False

    # Prompt and wait for valid input
    while not load_flag:
        print("\nPlease enter the file you would like to process."
              "\nRemember to include the file extension (.txt).")
        load_file = raw_input("\nFile Name: ")

        # Makes sure file is accessible
        if not os.access(load_file, os.R_OK):
            print "\n%s is not accessible." % load_file
            print "Please try again. The file you use must be in the same folder as this script\n" \
                  "or have the file path."

        # good input entered
        else:
            load_flag = True

    # read in ratios
    with open(load_file, 'r') as f:
        ratios = f.readlines()

    # split ratios into proper values
    for i in range(0, len(ratios)):
        ratios[i] = ratios[i].split(', ')

    # Cast to correct type
    ratios[0] = map(lambda x: float(x), ratios[0])
    ratios[1] = map(lambda x: float(x), ratios[1])
    ratios[2] = map(lambda x: x == 'True', ratios[2])
    ratios[3] = map(lambda x: float(x), ratios[3])

    print '\nData loaded.\nYour plots will now be generated.'

    plotType = ''

    # Get input for what type of plot(s) to generate
    while plotType != 'done':

        plotType = raw_input("\nEnter 'done' to advance or enter a plot type to generate that plot."
                             "\nPlot options are 'scatter', 'heatmap', and '3d'.\nEnter input: ")

        # If a good plot type is entered, this will generate the desired result
        try:
            if plotType != 'done':
                print '\nThis may take a moment to make your positive mode plot.' \
                      '\nBe sure to save your plot then close it to continue.'
                plotVanK(ratiosList=ratios, typeOfPlot=plotType)

        # this catches invalid options and reprompts
        except IOError:
            if plotType != 'done':
                print '\nIncorrect input. Please enter a valid input.'
            pass

# This shouldn't ever run but if there's something that was missed, this will catch it.
else:
    print 'An unexpected input was provided'
    raise IOError

print('done')
