
import os
import re

class Table:
    def __init__(self, fileName: str, filePath: str):
        self.tableName = fileName[:-4]
        print(self.tableName)

        fileContent = open(filePath, 'r')

        # Creating a matrix with all the info
        rowQnt = 0
        dataInFile = []
        for line in fileContent:
            dataInFile.append(line.split(","))
            rowQnt += 1

        # Removes '\n' from the last collumn
        iterator = 0
        lastCol = len(dataInFile[0]) - 1
        while iterator < rowQnt:
            string = dataInFile[iterator][lastCol]
            dataInFile[iterator][lastCol] = string[:-1]

            iterator += 1

        self.collumnNames = dataInFile[0]
        self.tableContent = dataInFile[1:]