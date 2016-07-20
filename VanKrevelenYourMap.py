'''
Takes a csv as an input and works through the compounds to extract the number of C, H, and O
present. It also notes if N is present and marks those points, then calculates the ratios of
H:C and O:C and plots them and generates a Heatmap based on a second csv input.
'''
import os
import sys

import matplotlib.pyplot as plt

import heatmap
from extractNeededElementalData import extract_needed_elemental_data
from processElementalData import process_elemental_data

#TODO this will need some overhauling because the plot takes two inputs not one...
def compareXY(XY1, XY2):
    '''
    Little function to make the testing to see if the points are close a bit easier.
    '''

    # These define what is close enough to count. If you're not satisfied with the script's
    # heatmapping, this is a good place to start making adjustments to its sensitivity.
    X_ADJUST = .20
    Y_ADJUST = .15

    okay = False

    # Checks if one point is +/- the adjust values
    if XY2[0] + X_ADJUST > XY1[0] > XY2[0] - X_ADJUST:
        if XY2[1] + Y_ADJUST > XY1[1] > XY2[1] - Y_ADJUST:
            okay = True

    return okay

# usage_mesg = 'VanKrevelenYourMap.py <file to plot> <file for map>'
#
# # Checks if files are available.
# filename_txt = sys.argv[1]
# if not os.access(filename_txt, os.R_OK):
#     print "%s is not accessible." % filename_txt
#     print usage_mesg
#     sys.exit(1)
#
# filename_txt = sys.argv[2]
# if not os.access(filename_txt, os.R_OK):
#     print "%s is not accessible." % filename_txt
#     print usage_mesg
#     sys.exit(1)
#
# # If the right number of inputs are provided then run the analysis for both data sets
# if(len(sys.argv) == 3 ):
#
#     # Processes file to plot (top layer)
#     filename_txt_plot = sys.argv[1]
#     elementalList_plot = extract_needed_elemental_data(filename_txt_plot)
#     ratiosList_plot = process_elemental_data(elementalList_plot)
#
#     # Processes file to map (bottom image)
#     filename_txt_map = sys.argv[2]
#     elementalList_map = extract_needed_elemental_data(filename_txt_map)
#     ratiosList_map = process_elemental_data(elementalList_map)
# VanKrevelen scatter mapped over heat map
def plotYourMap(ratiosList_map, ratiosList_plot):

    # Another good area to adjust configurations. This is the percent of nodes that
    # must be within +/- the adjust range of a point for it to be added to the heatmap.
    PERCENT_NEAR = .15

    # Turns list into tuple pairs for use in the heatmap function
    y = 0
    tList = []
    for x in ratiosList_map[1]:
        tHelp = (x, ratiosList_map[0][y])
        tList.append(tHelp)
        y += 1

    filtered_tuples = []

    # Uses the percent near to filter values and add to a tuple
    for pair in tList:
        counter = 0

        for compare_pair in tList:
            if compareXY(pair, compare_pair):
                counter += 1
        if counter > (len(tList) * PERCENT_NEAR):
            filtered_tuples.append(pair)

    # Generates Heatmap
    hm = heatmap.Heatmap()
    img = hm.heatmap(filtered_tuples, dotsize=100, opacity=250, scheme='classic', area=((0, 0), (1.8, 3.0)))

    # Graphs the data provided and labels axes
    fig = plt.figure()
    fig.suptitle('Van Krevelen Heatmap', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)

    ax.set_xlabel('O:C Ratio')
    ax.set_ylabel('H:C Ratio')

    # Creates a list for plotting purposes where two elements are lists of compounds with N and without respectively
    listByN = [[], []]
    withN = None
    withoutN = None
    for i in range(len(ratiosList_plot[2])):
        if ratiosList_plot[2][i]:
            listByN[0].append([ratiosList_plot[1][i],ratiosList_plot[0][i], 'r', '^'])
        else:
            listByN[1].append([ratiosList_plot[1][i],ratiosList_plot[0][i], 'b', 'o'])

    counter = 0
    for i in listByN:
        for j in i:
            if counter == 0:
               withN = plt.scatter(j[0], j[1], 15.0, j[2], j[3], alpha = .25)
            else:
                withoutN = plt.scatter(j[0], j[1], 15.0, j[2], j[3], alpha = .25)
        counter += 1

    # Adds in heatmap image as background image
    myaximage = ax.imshow(img, aspect='auto',extent=(0, 1.8, 0, 3.0), alpha=1, zorder=-1)

    # Shows legend.
    if withN and withoutN:
        plt.legend((withN, withoutN), ('Does have N', 'Does not have N'), scatterpoints = 1, loc='lower left', ncol=1, fontsize=9)

    plt.show()

    print "Done!"

