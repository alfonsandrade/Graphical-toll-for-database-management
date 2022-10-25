
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
        print(self.collumnNames)
        self.tableContent = dataInFile[1:]

        self.attributesCasting()

        fileContent.close()


    # Makes the conversion of data to int or float, when necessary
    def attributesCasting(self):
        iterator = 0
        while iterator < len(self.collumnNames):
            try:
                self.tableContent[0][iterator] = int(self.tableContent[0][iterator])
                rowIterator = 1
                while rowIterator < len(self.tableContent):
                    self.tableContent[rowIterator][iterator] = int(self.tableContent[rowIterator][iterator])
                    rowIterator += 1

                iterator += 1
                continue
            except:
                pass

            try:
                self.tableContent[0][iterator] = float(self.tableContent[0][iterator])
                rowIterator = 1
                while rowIterator < len(self.tableContent):
                    self.tableContent[rowIterator][iterator] = float(self.tableContent[rowIterator][iterator])
                    rowIterator += 1

                iterator += 1
                continue
            except:
                pass

            iterator += 1

        return