# Function to plot correct version of VanKrevelen based on input.

from VanKrevelen import plotVanKrevelen
from VanKrevelenHeatmap import plotHeatmap
from VanKrevelenSideBySide import plotSideBySide
from VanKrevelenYourMap import plotYourMap


# This function simply routes the input to the correct plotting function
def plotVanK(ratiosList, typeOfPlot='scatter', secondaryList=None):

    # makes sure case doesn't impact input
    typeOfPlot = typeOfPlot.lower()

    # generates plot using generic scatter method
    if typeOfPlot == 'scatter':

        plotVanKrevelen(ratiosList)

    # generates a heatmap
    elif typeOfPlot == 'heatmap':

        plotHeatmap(ratiosList)

    # generates a 3d (SideBySide) map
    elif typeOfPlot == '3d':

        plotSideBySide(ratiosList)

    # Generates a heatmap using the ratiosList as the heat map input and the secondary list as the scatter input
    elif typeOfPlot == 'yourmap':

        plotYourMap(ratiosList, secondaryList)

    else:
        raise IOError
