
import os
import re

class Table:
    def __init__(self, fileName: str, filePath: str):
        self.tableName = fileName - ".csv"

        fileContent = open(filePath, 'r')

        # Creating a matrix with all the info
        rowQnt = 0
        dataInFile = []
        for line in fileContent:
            dataInFile.append(line.split(","))
            rowQnt += 1

        # Removes '\n' from the last collumn
        iterator = 0
        colQnt = len(dataInFile[0])
        while iterator < rowQnt:
            string = dataInFile[iterator][colQnt]
            dataInFile[iterator][colQnt] = string[:-1]

            iterator += 1

        self.collumnNames = dataInFile[0]
        self.tableContent = dataInFile[1:]