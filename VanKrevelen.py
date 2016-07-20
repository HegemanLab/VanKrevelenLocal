'''
Takes a csv as an input and works through the compounds to extract the number of C, H, and O
present. It also notes if N is present and marks those points, then call a method to calculate
the ratios of H:C and O:C and plots them.
'''
import os
import sys

import matplotlib.pyplot as plt

from extractNeededElementalData import extract_needed_elemental_data
from processElementalData import process_elemental_data

# usage_mesg = 'VanKrevelen.py <txt file(s)>'
#
# # Checks if files are available.
# filename_txt = sys.argv[1]
# if not os.access(filename_txt, os.R_OK):
#     print "%s is not accessible." % filename_txt
#     print usage_mesg
#     sys.exit(1)
#
#
# # If two arguments were given
# if len(sys.argv) == 2:
#
#     # Assigns filename to the second argument provided in the command prompt
#     filename_txt = sys.argv[1]
#
#     # Gets complete list of all element counts in all compounds identified
#     elementalList = extract_needed_elemental_data(filename_txt)
#
#     # Gets complete list of ratios (also contains boolean for presence of nitrogen
#     ratios_list = process_elemental_data(elementalList)
# #TODO switch this back (unindent the section below and remove function call)
#

# Graphs the data provided and labels axes
def plotVanKrevelen(ratios_list):
    area = 10.0

    fig = plt.figure()
    fig.suptitle('Van Krevelen Diagram', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    plt.xlim(0, 1.8)
    plt.ylim(0, 3.0)

    ax.set_xlabel('O:C Ratio')
    ax.set_ylabel('H:C Ratio')

    # Creates a list for plotting purposes where two elements are lists of compounds with N and without respectively
    listByN = [[], []]

    for i in range(len(ratios_list[2])):
        if ratios_list[2][i]:

            # Plots elements with nitrogen as red ('r') triangles ('^')
            listByN[0].append([ratios_list[1][i], ratios_list[0][i], 'r', '^'])
        else:

            # Plots elements without nitrogen as blue ('b') circles ('o')
            listByN[1].append([ratios_list[1][i], ratios_list[0][i], 'b', 'o'])

    # Creates plots by individually plotting values with N or with out N.
    withN = None
    withoutN = None

    counter = 0
    for i in listByN:
        for j in i:
            if counter == 0:
                withN = plt.scatter(j[0], j[1], 15.0, j[2], j[3], alpha=.25)
            else:
                withoutN = plt.scatter(j[0], j[1], 15.0, j[2], j[3], alpha=.25)
        counter += 1

    # Generates legend
    if withN and withoutN:
        plt.legend((withN, withoutN), ('Does have N', 'Does not have N'), scatterpoints=1, loc='lower left', ncol=1, fontsize=9)


    plt.show()

    print("done")
