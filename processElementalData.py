'''
Takes in list of values for C, H, O, and N and then computes the needed ratios and generates
booleans for presence of nitrogen.
'''


def process_elemental_data(elementalList):
    # 0 = H:C, 1 = O:C, 2 = Present/Not (True, False) 3 = N:C
    ratios_list = [[], [], [], []]

    # Computes all the ratios and adds them to the ratios_list
    for line in elementalList:
        if len(line) == 4:

            HtoC = line[1] / line[0]
            ratios_list[0].append(HtoC)
            OtoC = line[2] / line[0]
            ratios_list[1].append(OtoC)
            if line[3] == 0:
                ratios_list[2].append(False)
            else:
                ratios_list[2].append(True)
            NtoC = line[3] / line[0]
            ratios_list[3].append(NtoC)
    return ratios_list
