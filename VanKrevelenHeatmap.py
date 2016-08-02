'''
Takes a csv as an input and works through the compounds to extract the number of C, H, and O 
present. It also notes if N is present and marks those points, then calculates the ratios of
H:C and O:C and plots them and generates a Heatmap based on where the points cluster.
'''


import sys
import os
from extractNeededElementalData import extract_needed_elemental_data
from processElementalData import process_elemental_data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import six
import dateutil
import itertools
import heatmap



def compareXY(XY1, XY2):
    '''
    Little function to make the testing to see if the points are close a bit easier.
    '''

    # These define what is close enough to count. If you're not satisfied with the script's
    # heatmapping, this is a good place to start making adjustments.
    X_ADJUST = .20
    Y_ADJUST = .15

    okay = False

    # Checks if one point is +/- the adjust values
    if XY1[0] < XY2[0] + X_ADJUST and XY1[0] > XY2[0] - X_ADJUST:
        if XY1[1] < XY2[1] + Y_ADJUST and XY1[1] > XY2[1] - Y_ADJUST:
            okay = True
 
    return okay


def plotHeatmap(ratiosList):
    # Another good area to adjust configurations. This is the percent of nodes that
    # must be within +/- the adjust range of a point for it to be added to the heatmap.
    PERCENT_NEAR = .15

    # Turns list into tuple pairs for use in the heatmap function
    y = 0
    tList = []
    for x in ratiosList[1]:
        tHelp = (x, ratiosList[0][y])
        tList.append(tHelp)
        y += 1

    filteredtups = []

    # Uses the percent near to filter values and add to a tuple
    for pair in tList:
        counter = 0
        for compair in tList:
            if compareXY(pair, compair):
                counter += 1
        if counter > (len(tList) * PERCENT_NEAR):
            filteredtups.append(pair)

    # Generates Heatmap
    hm = heatmap.Heatmap()
    img = hm.heatmap(filteredtups, dotsize = 100, opacity = 250, scheme='classic', area=((0,0),(1.8,3.0)))

    # Graphs the data provided and labels axes
    fig = plt.figure()
    fig.suptitle('Van Krevelen Heatmap', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    plt.xlim(0, 1.8)
    plt.ylim(0, 3.0)

    ax.set_xlabel('O:C Ratio')
    ax.set_ylabel('H:C Ratio')

    # Creates a list for plotting purposes where two elements are lists of compounds with N and without respectively
    '''
    Remove these comments to plot the points in addition to seeing the heatmap itself.
    Note, this will slow up the runtime of the program a fair amount.

    listByN = [[], []]
    withN = None
    withoutN = None
    for i in range(len(ratios_list[2])):
        if ratios_list[2][i]:
            listByN[0].append([ratios_list[1][i],ratios_list[0][i], 'r', '^'])
        else:
            listByN[1].append([ratios_list[1][i],ratios_list[0][i], 'b', 'o'])

    counter = 0
    for i in listByN:
        for j in i:
            if counter == 0:
               withN = plt.scatter(j[0], j[1], 15.0, j[2], j[3], alpha = .25)
            else:
                withoutN = plt.scatter(j[0], j[1], 15.0, j[2], j[3], alpha = .25)
        counter += 1
    '''
    myaximage = ax.imshow(img, aspect='auto', extent=(0, 1.8, 0, 3.0), alpha=1, zorder=-1)

    # Remove this comment if you want to see a legend when actually plotting the points.
    # plt.legend((withN, withoutN), ('Does have N', 'Does not have N'), scatterpoints = 1, loc='lower left', ncol=1,fontsize = 9)

    plt.show()

    print "Done!"

'''
Uncomment this section if you wish to run this script using the BMRB online data base and use the more
flexible commandline options.

usage_mesg = 'VanKrevelenHeatmap.py <txt file(s)>'

# Checks if files are available.

# filename_txt = "example-compounds-pos.txt"
filename_txt = sys.argv[1]
if(not os.access(filename_txt, os.R_OK)):
    print "%s is not accessible." % filename_txt
    print usage_mesg
    sys.exit(1)


if(len(sys.argv) == 2 ):
   filename_txt = sys.argv[1]

elementalList = extract_needed_elemental_data(filename_txt)
ratiosList = process_elemental_data(elementalList)
plotHeatmap(ratiosList)
'''

























