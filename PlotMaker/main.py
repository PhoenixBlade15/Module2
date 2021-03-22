import os
from os import path
import matplotlib.pyplot as plt
import urllib.request
# Get the raw urls needed - TO DO


def saveBenchmark(currentGameName, benchmarkInfo):
    gameNames.append(currentGameName)

    # Finds the correct folder to put the benchmark into
    fileDir = currentGameName[currentGameName.index(' ') + 1:]
    fileDir = fileDir[:fileDir.index(" ")] + "/"

    # Checks if folder already exists and if not make it
    if not path.exists(fileDir):
        os.mkdir(fileDir, 0o666)

    # Checks if the text file exists if so delete it
    if path.exists(fileDir + currentGameName):
        os.remove(fileDir + currentGameName)
        # print(dir + currentGameName + " removed.")

    # Creates and writes to a new text file in the folder and name of the game benchmark
    gameText = open(fileDir + currentGameName, 'x')
    gameText.write(benchmarkInfo)
    gameText.close()


def plotGraph(workingList, currentGameName, currentHardware):
    for game in workingList:

        # Gets identifiers from the name of the game for plot
        resolution = game[game.index(" ") + 1:]
        resolution = resolution[resolution.index(" ") + 1: -4]
        gameInfo = open(currentGameName + "/" + game, 'r')

        # Loops through the information in the game benchmark files
        for line in gameInfo:

            # Gets the important information from the line of the game
            labelOfLine = line[:line.index(":")].strip()
            frameRate = [float(line[line.index(":") + 1:-4].strip())]
            y = [resolution]

            # Determines what color to set the dot to
            if labelOfLine == "Average framerate":
                colorOf = "ro"
            elif labelOfLine == "Minimum framerate":
                colorOf = "bo"
            elif labelOfLine == "Maximum framerate":
                colorOf = "go"
            elif labelOfLine == "1% low framerate":
                colorOf = "co"
            elif labelOfLine == "0.1% low framerate":
                colorOf = "mo"

            # Will plot the dot onto the graph and if the label is not already in the legend add it
            plt.plot(y, frameRate, colorOf,
                     label=labelOfLine if labelOfLine not in plt.gca().get_legend_handles_labels()[1] else '')

            # Gives a title and labels both x and y axis
            plt.title("Benchmark of " + currentGameName)
            plt.xlabel('Resolution', color='#1C2833')
            plt.ylabel('Frame Rate(Higher is better)', color='#1C2833')
        gameInfo.close()

    # Puts the legend onto the graph, saves the graph, and then closes the graph to reuse elsewhere
    plt.legend()
    plt.savefig(currentGameName + "/" + currentHardware + "" + currentGameName + ".png")
    plt.close()


urlList = ["https://raw.githubusercontent.com/wendelltron/csc496demo/master/5950x/Reference%206700XT/Benchmark.txt",
           "https://raw.githubusercontent.com/wendelltron/csc496demo/master/5950x/Sapphire%206700XT/Benchmark.txt"]
benchmarksTextConjoined = []

# Downloads all the text files from urls gathered in the previous step
for url in urlList:
    # Cuts the first part off to give us the cpu and then gpu and file name
    textFileName = url[64:]
    textFileName = textFileName.replace('/', '').replace('%20', '')
    # Checks if the file exists and if so delete it
    if path.exists(textFileName):
        os.remove(textFileName)
        # print(textFileName + " removed.")
        # Save the text file in the url as the name and add it to a list
    urllib.request.urlretrieve(url, textFileName)
    benchmarksTextConjoined.append(textFileName)

currentGameName = ""
gameNames = []
benchmarkInfo = ""

# Separate the conjoined benchmarks
for benchmarks in benchmarksTextConjoined:
    file = open(benchmarks, "r")
    for line in file:
        # Makes sure the line is not empty
        if line != "\n":
            if line[0] != " ":

                # Isolate the game name from the string
                gameName = line[line.index(' ')+1:]
                gameName = gameName[gameName.index(' ')+1:]
                gameName = gameName[:gameName.index(' ')-4]

                # Gets the resolution out of the line name
                resolution = line
                for i in range(0, 11):
                    resolution = resolution[resolution.index(' ')+1:]
                resolution = resolution.replace(' ', '')

                # Adds the items together to have an identifier
                fullName = benchmarks[:-4] + " " + gameName + " " + resolution.replace("\n", "") + ".txt"

                # Checks if first game or not
                if currentGameName == "":
                    currentGameName = fullName

                # Checks if the game name has switched
                if currentGameName != fullName:
                    gameNames.append(currentGameName)
                    saveBenchmark(currentGameName, benchmarkInfo)
                    benchmarkInfo = ""
                    currentGameName = fullName
                # Reads the next 5 lines to grab the info for that file
                for x in range(0, 5):
                    benchmarkInfo = benchmarkInfo + file.readline().strip() + "\n"
    file.close()
    saveBenchmark(currentGameName, benchmarkInfo)

currentGameName = ""
currentHardware = ""
workingList = []

# Check benchmark and game name is same
for gameFile in gameNames:

    # Grabs the information needed to identify what benchmark we are on
    hardware = gameFile[:gameFile.index(" ")]
    gameName = gameFile[gameFile.index(" ")+1:]
    gameName = gameName[:gameName.index(" ")]

    # Checks if the first iteration or a different benchmark and adjusts
    if currentHardware == "":
        currentHardware = hardware
    if currentGameName == "":
        currentGameName = gameName
    if currentGameName == gameName and currentHardware == hardware:
        workingList.append(gameFile)
    else:
        plotGraph(workingList, currentGameName, currentHardware)

        # Sets up the next benchmark
        workingList = [gameFile]
        currentHardware = hardware
        currentGameName = gameName
plotGraph(workingList, currentGameName, currentHardware)

# Removes all the unneeded text files
for gameFile in gameNames:
    gameName = gameFile[gameFile.index(" ")+1:]
    gameName = gameName[:gameName.index(" ")]
    fileDir = gameName + "/" + gameFile
    if path.exists(fileDir):
        os.remove(fileDir)
