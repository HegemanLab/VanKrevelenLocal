'''
Writes needed information to a .txt file with either -neg or -pos depending on type of scan.
This function is only used if you decide to use this package in coordination with the BMRB website (non-local).
'''


def writeTxt(inputList, filename, polarity):
    # if it's an mzxml/mzXML file
    if filename[len(filename) - 3].lower() == 'x':
        filename = filename[:len(filename) - 6]

    # else it's an mzML file
    else:
        filename = filename[:len(filename) - 5]

    # Determine which list is being written
    if polarity == 1:
        newFile = open(filename + "-pos.txt", "w")
        for i in inputList:
            newFile.write(str(i) + "\n")

    if polarity == 0:
        newFile = open(filename + "-neg.txt", "w")
        for i in inputList:
            newFile.write(str(i) + "\n")
