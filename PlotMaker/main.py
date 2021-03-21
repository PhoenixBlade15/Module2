import os
import shutil
from os import path
import matplotlib.pyplot as plt
import numpy as np
import urllib.request

# Get the raw urls needed
# Download Files
# Separate values from benchmark.txt
# Plot each benchmark

urlList = ["https://raw.githubusercontent.com/wendelltron/csc496demo/master/5950x/Reference%206700XT/Benchmark.txt", "https://raw.githubusercontent.com/wendelltron/csc496demo/master/5950x/Sapphire%206700XT/Benchmark.txt"]
benchmarksTextConjoined = []
gameNames = []
currentGameName = ""
benchmarkInfo = ""

# Downloads all the text files from urls gathered in the previous step
for url in urlList:
    # Cuts the first part off to give us the cpu and then gpu and file name
    textFileName = url[64:]
    textFileName = textFileName.replace('/', '').replace('%20', '')
    # Checks if the file exists and if so delete it
    if path.exists(textFileName):
        os.remove(textFileName)
        print(textFileName + " removed.")
        # Save the text file in the url as the name and add it to a list
    urllib.request.urlretrieve(url, textFileName)
    benchmarksTextConjoined.append(textFileName)

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

                    # Finds the correct folder to put the benchmark into
                    dir = currentGameName[currentGameName.index(' ')+1:]
                    dir = dir[:dir.index(" ")] + "/"

                    # Checks if folder already exists and if not make it
                    if not path.exists(dir):
                        os.mkdir(dir, 0o666)

                    # Checks if the text file exists if so delete it
                    if path.exists(dir + currentGameName):
                        os.remove(dir + currentGameName)

                    # Creates and writes to a new text file in the folder and name of the game benchmark
                    gameText = open(dir + currentGameName, 'x')
                    gameText.write(benchmarkInfo)
                    gameText.close()
                    currentGameName = fullName
                else:
                    # Reads the next 5 lines to grab the info for that file
                    for x in range(0, 5):
                        benchmarkInfo = benchmarkInfo + file.readline().strip() + "\n"
    file.close()
