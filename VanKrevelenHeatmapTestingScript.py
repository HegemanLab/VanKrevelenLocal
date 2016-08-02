'''
Runs a batch of .csv files to generate multiple heatmaps. This code is less commented but
operates mostly the same as the VanKrevelenHeatmap.py script so consult that if more
help is needed. Also, this script operates in the workflow that goes out to the BMRB database, not the local
workflow.
'''


import matplotlib.pyplot as plt
import heatmap
from extractNeededElementalData import extract_needed_elemental_data
from processElementalData import process_elemental_data


# Your file names go here
mappingFiles = ["example-neg.txt"]

def compareXY(XY1, XY2):
    '''
    Little function to make the testing to see if the points are close a bit easier.
    '''

    # These define what is close enough to count
    X_ADJUST = .20
    Y_ADJUST = .15

    okay = False

    if XY2[0] - X_ADJUST < XY1[0] < XY2[0] + X_ADJUST:
        if XY2[1] - Y_ADJUST < XY1[1] < XY2[1] + Y_ADJUST:
            okay = True
 
    return okay

for files in mappingFiles:
    filename_txt = files
    elementalList = extract_needed_elemental_data(filename_txt)
    ratiosList = process_elemental_data(elementalList)

    PERCENT_NEAR = .15

    y = 0
    tList = []
    for x in ratiosList[1]:
        tHelp = (x, ratiosList[0][y])
        tList.append(tHelp)
        y += 1

    filtered_tuples = []

    for pair in tList:
        counter = 0
        for compare_pair in tList:
            if compareXY(pair, compare_pair):
                counter += 1
        if counter > (len(tList) * PERCENT_NEAR):
            filtered_tuples.append(pair)

    hm = heatmap.Heatmap()
    img = hm.heatmap(filtered_tuples, dotsize=100, opacity=250, scheme='classic', area=((0, 0), (1.8, 3.0)))

    # Graphs the data provided and labels axes

    fig = plt.figure()
    fig.suptitle('Van Krevelen Heatmap', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)

    ax.set_xlabel('O:C Ratio')
    ax.set_ylabel('H:C Ratio')

    '''
    Remove these comments to plot the actual points in addition to the heat patterns.

    # Creates a list for plotting purposes where two elements are lists of compounds with N and without respectively
    listByN = [[],[]]
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

    myaximage = ax.imshow(img, aspect='auto' ,extent=(0, 1.8, 0, 3.0), alpha=1, zorder=-1)

    # NOTE: Figures saved, not displayed.
    plt.savefig(files[:len(files) - 4] + ".pdf")

    print "done with " + files
print "Done!"


























