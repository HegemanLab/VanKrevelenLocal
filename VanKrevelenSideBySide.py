'''
Takes a csv as an input and works through the compounds to extract the number of C, H, O, and N
present. It also notes if N is present and marks those points, then calculates the ratios of
H:C, O:C, and N:C and plots them and generates side by side 3D plots to create a stereoscopic
effect. Note graphics should be approximately 6 cm apart so adjustments may need to be made
based on the size screen you are working on.
'''

import os
import sys

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from extractNeededElementalData import extract_needed_elemental_data
from processElementalData import process_elemental_data

# usage_mesg = 'VanKrevelenSideBySide.py <txt file(s)>'
#
#
# # Checks if files are available.
# filename_txt = sys.argv[1]
# if not os.access(filename_txt, os.R_OK):
#     print "%s is not accessible." % filename_txt
#     print usage_mesg
#     sys.exit(1)
#
# # Checks if the right number of arguments are provided.
# if len(sys.argv) == 2:
#     filename_txt = sys.argv[1]
#     elementalList = extract_needed_elemental_data(filename_txt)
#     ratiosList = process_elemental_data(elementalList)


# Graphs the data provided and labels axes
def plotSideBySide(ratiosList):
    area = 10.0

    fig = plt.figure(figsize=(17, 7))
    fig.suptitle('Van Krevelen Diagram - Side By Side', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(121, projection='3d')

    ax.set_xlabel('O:C Ratio')
    ax.set_ylabel('H:C Ratio')
    ax.set_zlabel('N:C Ratio')

    # Creates a list for plotting purposes where two elements are lists of compounds with N and without respectively
    listByN = [[], []]
    withN = None
    withoutN = None
    for i in range(len(ratiosList[2])):
        if ratiosList[2][i]:
            listByN[0].append([ratiosList[1][i], ratiosList[0][i], ratiosList[3][i], 'r', '^'])
        else:
            listByN[1].append([ratiosList[1][i], ratiosList[0][i], ratiosList[3][i], 'b', 'o'])

    counter = 0
    for i in listByN:
        for j in i:
            if counter == 0:
                withN = ax.scatter(xs=j[0], ys=j[1], zs=j[2], s=15.0, c=j[3], marker=j[4], alpha=.25)
            else:
                withoutN = ax.scatter(xs=j[0], ys=j[1], zs=j[2], s=15.0, c=j[3], marker=j[4], alpha=.25)
        counter += 1

    if withoutN and withN:
        plt.legend((withN, withoutN), ('Does have N', 'Does not have N'), scatterpoints=1, loc='lower left', ncol=1, fontsize=9)

    '''
    Second plot rotated 6 degrees per stereoscopic best practices.
    '''
    ax2 = fig.add_subplot(122, projection='3d')

    ax2.set_xlabel('O:C Ratio')
    ax2.set_ylabel('H:C Ratio')
    ax2.set_zlabel('N:C Ratio')

    withoutN = None
    withN = None

    counter = 0
    for i in listByN:
        for j in i:
            if counter == 0:
                withN = ax2.scatter(xs=j[0], ys=j[1], zs=j[2], s=15.0, c=j[3], marker=j[4], alpha=.25)
            else:
                withoutN = ax2.scatter(xs=j[0], ys=j[1], zs=j[2], s=15.0, c=j[3], marker=j[4], alpha=.25)
        counter += 1

    ax2.azim -= 6

    if withN and withoutN:
        plt.legend((withN, withoutN), ('Does have N', 'Does not have N'), scatterpoints=1, loc='lower left', ncol=1, fontsize=9)


    plt.tight_layout(w_pad=.18)

    '''
    If you would rather not display the file and just want to save it in a specific format, remove the comment from the
    line below (delete the first #) and comment out the next line (add a # to the front of the line of code that says
    plt.show()).
    '''

    # plt.save("filename.pdf") # or whatever file type you need.
    plt.show()

    print("done")
