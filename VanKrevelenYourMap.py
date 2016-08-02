'''
Takes a csv as an input and works through the compounds to extract the number of C, H, and O
present. It also notes if N is present and marks those points, then calculates the ratios of
H:C and O:C and plots them and generates a Heatmap based on a second csv input.

Due to taking two inputs, this plotting option was left out of the commandline aggregate tool
however, it can still be used by saving the ratios lists to files, reading them in in the command
line or through another script, and then using those as parameters to the core function of this script.
'''


import matplotlib.pyplot as plt
import heatmap


# Little function to make the testing to see if the points are close a bit easier.
def compareXY(XY1, XY2):

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

# function for plotting one set of ratios as a heat map and the other as a scatter
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

