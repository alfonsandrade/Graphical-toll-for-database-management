#   Graphical toll for  database  query execution
#                   Made by:
#       João Vitor Caversan dos Passos
#   Contact: joaopassos@alunos.utfpr.edu.br
#   Alfons Carlos César Heiermann de Andrade
#       Contact: alfons@alunos.utfpr.edu.br

import sys
import os

sys.setrecursionlimit(1000)

from Table  import Table
from Parser import Parser

class Database:
    def __init__(self, dirPath : str):
        self.tables = []
        tablesIterator = 0

        for root, direcs, files in os.walk(dirPath):
            for file in files:
                filePath = os.path.join(root, file)

                if filePath.endswith(".csv"):
                    newTable = Table(file, filePath)
                    self.tables.append(newTable)
                    tablesIterator += 1

        # Creates dictionary to store comparation functions for each operand
        self.operatorsDict = {}
        self.operatorsDict["="]   = lambda a, b: a == b
        self.operatorsDict["!="]  = lambda a, b: a != b
        self.operatorsDict["<"]   = lambda a, b: a < b
        self.operatorsDict[">"]   = lambda a, b: a > b
        self.operatorsDict[">="]  = lambda a, b: a >= b
        self.operatorsDict["<="]  = lambda a, b: a <= b
        self.operatorsDict["&"]   = lambda a, b: a & b
        self.operatorsDict["|"]   = lambda a, b: a | b

    def searchLoop(self):
        query = "nop"
        whatToSelect = []
        selectFrom   = []
        where        = []
        order_by     = []
        tablesToJoin = []
        joinEquality = []
        parser       = Parser()

        print("\nThis DB tool uses spaces as a separator for all words and symbols. Don't forget the ; in the end \nYou may now write your queries:\n")

        # Mainloop for searching in database
        while query[0] != "quit;":
            print("> ", end = '')
            query = input()
            query = query.split(' ')

            if query[0] == "quit;":
                break

            print(query)

            isQueryOk = parser.verifyPointCommaInTheEnd(query)
            if isQueryOk is False:
                continue

            result = parser.queryTreatment(query)

            whatToSelect = result[0]
            selectFrom   = result[1]
            where        = result[2]
            order_by     = result[3]
            tablesToJoin = result[4]
            joinEquality = result[5]

            print(whatToSelect)
            print(selectFrom  )
            print(where       )
            print(order_by    )
            print(tablesToJoin)
            print(joinEquality)

            isQueryOk = parser.isQuerySyntaxOk(self.tables, whatToSelect, selectFrom, where, order_by, tablesToJoin, joinEquality)
            if isQueryOk is False:
                continue

            if whatToSelect[0] == "*":
                if where == [] and order_by == []:
                    # Select * from chosen
                    self.selectAllFrom(selectFrom)
                elif where == []:
                    # Select * from chosen order by chum
                    self.selectAllFromOrderBy(selectFrom, order_by)
                elif order_by == []:
                    # Select * from chosen where lalos < ligos
                    self.selectAllFromWhere(selectFrom, where)
                else:
                    # Select * from chosen where paosdvaso order by oasivaosi
                    self.selectAllFromWhereOrderBy(selectFrom, where, order_by)
            else:
                if where == [] and order_by == []:
                    self.selectSomethingFrom(whatToSelect, selectFrom)
                elif where == []:
                    self.selectSomethingFromOrderBy(whatToSelect, selectFrom, order_by)
                elif order_by == []:
                    self.selectSomethingFromWhere(whatToSelect, selectFrom, where)
                else:
                    self.selectSomethingFromWhereOrderBy(whatToSelect, selectFrom, where, order_by)

        print("Bye")

        return

    ##################################################################################
    ########################## QUERY ALGORYTHMS WITH * ###############################
    ##################################################################################

    # select * from something
    def selectAllFrom(self, selectFrom, tablesToJoin, joinEquality):
        tablesToUse  = []
        tableToPrint = []

        if tablesToJoin == []:
            for table in self.tables:
                if table.tableName == selectFrom[0]:
                    tablesToUse.append(table)
                    tableToPrint = table.tableContent

        for table in tablesToUse:
            print("|                " + table.tableName + "                |", end = '')
        print('')
        print("|", end = '')
        for table in tablesToUse:
            for collum in table.collumnNames:
                print("  "+ collum + "  |", end = '')
        print("")
        for line in tableToPrint:
            print(line)

        print("\n")

    # select * from something order by something
    def selectAllFromOrderBy(self, selectFrom, order_by, tablesToJoin, joinEquality):
        for table in self.tables:
            if table.tableName == selectFrom[0]:
                tableToUse = table

        orderedTable = self.mergeSortByCollumn(tableToUse.tableContent, 0, len(tableToUse.tableContent)-1, tableToUse.collumnNames[order_by[0]])

        if orderedTable != []:
            print("|                " + tableToUse.tableName + "                |")
            print("|", end = '')
            for line in tableToUse.collumnNames:
                print("  "+line + "  |", end = '')
            print("")
            for line in orderedTable:
                print(line)
        else:
            print("This relation is empty.")

    # select * from something where something < 78
    def selectAllFromWhere(self, selectFrom, where, tablesToJoin, joinEquality):
        for table in self.tables:
            if table.tableName == selectFrom[0]:
                tableToUse = table

        filteredTable = self.manageWhere(where, tableToUse)

        if filteredTable != []:
            print("|                " + tableToUse.tableName + "                |")
            print("|", end = '')
            for line in tableToUse.collumnNames:
                print("  "+line + "  |", end = '')
            print("")
            for line in filteredTable:
                print(line)
        else:
            print("This relation is empty.")

        print("\n")

    def selectAllFromWhereOrderBy(self, selectFrom, where, order_by, tablesToJoin, joinEquality):
        for table in self.tables:
            if table.tableName == selectFrom[0]:
                tableToUse = table

        filteredTable = self.manageWhere(where, tableToUse)
        filteredTable = self.mergeSortByCollumn(filteredTable, 0, len(filteredTable)-1, tableToUse.collumnNames[order_by[0]])

        if filteredTable != []:
            print("|                " + tableToUse.tableName + "                |")
            print("|", end = '')
            for line in tableToUse.collumnNames:
                print("  "+line + "  |", end = '')
            print("")
            for line in filteredTable:
                print(line)
        else:
            print("This relation is empty.")

        print("\n")

    ################################################################################
    ########################## QUERY ALGORITHMS WITHOUT * ##########################
    ################################################################################

    def selectSomethingFrom(self, whatToSelect, selectFrom, tablesToJoin, joinEquality):
        for table in self.tables:
            if table.tableName == selectFrom[0]:
                tableToUse = table

        print("|                " + tableToUse.tableName + "                |")
        print("|", end = '')

        for attribute in whatToSelect:
            print("  " + attribute + "  |", end = '')
        print("")

        for line in tableToUse.tableContent:
            print('|',  end = '')
            for attribute in whatToSelect:
                print("  ", end = "")
                print(line[tableToUse.collumnNames[attribute]], end = "")
                print("  |", end = '')
            print('')

        print("\n")

    def selectSomethingFromOrderBy(self, whatToSelect, selectFrom, order_by, tablesToJoin, joinEquality):
        for table in self.tables:
            if table.tableName == selectFrom[0]:
                tableToUse = table

        orderedTable = self.mergeSortByCollumn(tableToUse.tableContent, 0, len(tableToUse.tableContent)-1, tableToUse.collumnNames[order_by[0]])

        print("|                " + tableToUse.tableName + "                |")
        print("|", end = '')

        for attribute in whatToSelect:
            print("  "+ attribute + "  |", end = '')
        print("")

        for line in orderedTable:
            print('|',  end = '')
            for attribute in whatToSelect:
                print("  ", end = "")
                print(line[tableToUse.collumnNames[attribute]], end = "")
                print("  |", end = '')
            print('')

        print("\n")

    def selectSomethingFromWhere(self, whatToSelect, selectFrom, where, tablesToJoin, joinEquality):
        for table in self.tables:
            if table.tableName == selectFrom[0]:
                tableToUse = table

        filteredTable = self.manageWhere(where, tableToUse)

        for attribute in whatToSelect:
            print("  "+ attribute + "  |", end = '')
        print("")

        for line in filteredTable:
            print('|',  end = '')
            for attribute in whatToSelect:
                print("  ", end = "")
                print(line[tableToUse.collumnNames[attribute]], end = "")
                print("  |", end = '')
            print('')

        print("\n")

    def selectSomethingFromWhereOrderBy(self, whatToSelect, selectFrom, where, order_by, tablesToJoin, joinEquality):
        for table in self.tables:
            if table.tableName == selectFrom[0]:
                tableToUse = table

        filteredTable = self.manageWhere(where, tableToUse)
        filteredTable = self.mergeSortByCollumn(filteredTable, 0, len(filteredTable)-1, tableToUse.collumnNames[order_by[0]])

        for attribute in whatToSelect:
            print("  "+ attribute + "  |", end = '')
        print("")

        for line in filteredTable:
            print('|',  end = '')
            for attribute in whatToSelect:
                print("  ", end = "")
                print(line[tableToUse.collumnNames[attribute]], end = "")
                print("  |", end = '')
            print('')

        print("\n")



    def mergeSortByCollumn(self, table, left: int, right: int, collumnNum: int):
        def telettubies(table, left: int, middle: int, right: int, collumnNum: int):
            i = left
            leftAux = left
            j = middle+1
            tableAux = [0] * len(table)
            while (i <= middle and j <= right):
                if table[i][collumnNum] <= table[j][collumnNum]:
                    tableAux[leftAux] = table[i]
                    leftAux += 1
                    i += 1
                else: # (table[j][collumnNum] < table[i][collumnNum]):
                    tableAux[leftAux] = table[j]
                    leftAux += 1
                    j += 1
            while i <= middle:
                tableAux[leftAux] = table[i]
                leftAux += 1
                i += 1
            while j <= right:
                tableAux[leftAux] = table[j]
                leftAux += 1
                j += 1

            i = left
            while i <= right:
                table[i] = tableAux[i]
                i += 1

            return table

        half = 0
        if left < right:
            half = (left+right)//2
            table = self.mergeSortByCollumn(table, left, half, collumnNum)
            table = self.mergeSortByCollumn(table, half+1, right, collumnNum)
            table = telettubies(table, left, half, right, collumnNum)

        return table

    def manageWhere(self, where, tableToUse):
        logicOperand        = []
        comparations        = []
        attributesToCompare = []
        andOr       = ["and", "or"]

        # Parses the where array
        for word in where:
            if word in self.operatorsDict:
                comparations.append(word)
            elif word.lower() in andOr:
                logicOperand.append(word.lower())
            else:
                attributesToCompare.append(word)

        valueSinalizer       = []
        qntOfValueAttributes = 0
        iterator = 0
        while iterator < len(attributesToCompare):
            if attributesToCompare[iterator] in tableToUse.collumnNames:
                valueSinalizer.append(0)
            else:
                valueSinalizer.append(1)
                try:
                    attributesToCompare[iterator] = int(attributesToCompare[iterator])
                except:
                    pass

                qntOfValueAttributes += 1

            iterator += 1

        if (logicOperand != [] and len(attributesToCompare) < 4) or (len(attributesToCompare) < 2):
            print("Not enought arguments to compare. \n")
            return []
        if qntOfValueAttributes > 2: # Comparing an int to another in using a table (?)
            print("There is an error in your sql sintax. \n")
            return []

        filteredTable = []
        if qntOfValueAttributes == 2:
            if valueSinalizer[0] == 1 and valueSinalizer[2] == 1:
                if logicOperand[0] == "and":
                    for row in tableToUse.tableContent:
                        if (self.operatorsDict[comparations[0]](attributesToCompare[0], row[tableToUse.collumnNames[attributesToCompare[1]]]) and self.operatorsDict[comparations[1]](attributesToCompare[2], row[tableToUse.collumnNames[attributesToCompare[3]]])):
                            filteredTable.append(row)
                elif logicOperand[0] == "or":
                    for row in tableToUse.tableContent:
                        if (self.operatorsDict[comparations[0]](attributesToCompare[0], row[tableToUse.collumnNames[attributesToCompare[1]]]) or self.operatorsDict[comparations[1]](attributesToCompare[2], row[tableToUse.collumnNames[attributesToCompare[3]]])):
                            filteredTable.append(row)
            elif valueSinalizer[1] == 1 and valueSinalizer[3] == 1:
                if logicOperand[0] == "and":
                    for row in tableToUse.tableContent:
                        if (self.operatorsDict[comparations[0]](row[tableToUse.collumnNames[attributesToCompare[0]]], attributesToCompare[1]) and self.operatorsDict[comparations[1]](row[tableToUse.collumnNames[attributesToCompare[2]]], attributesToCompare[3])):
                            filteredTable.append(row)
                elif logicOperand[0] == "or":
                    for row in tableToUse.tableContent:
                        if (self.operatorsDict[comparations[0]](row[tableToUse.collumnNames[attributesToCompare[0]]], attributesToCompare[1]) or self.operatorsDict[comparations[1]](row[tableToUse.collumnNames[attributesToCompare[2]]], attributesToCompare[3])):
                            filteredTable.append(row)
            elif valueSinalizer[1] == 1 and valueSinalizer[2] == 1:
                if logicOperand[0] == "and":
                    for row in tableToUse.tableContent:
                        if (self.operatorsDict[comparations[0]](row[tableToUse.collumnNames[attributesToCompare[0]]], attributesToCompare[1]) and self.operatorsDict[comparations[1]](attributesToCompare[2], row[tableToUse.collumnNames[attributesToCompare[3]]])):
                            filteredTable.append(row)
                elif logicOperand[0] == "or":
                    for row in tableToUse.tableContent:
                        if (self.operatorsDict[comparations[0]](row[tableToUse.collumnNames[attributesToCompare[0]]], attributesToCompare[1]) or self.operatorsDict[comparations[1]](attributesToCompare[2], row[tableToUse.collumnNames[attributesToCompare[3]]])):
                            filteredTable.append(row)
            else: # valueSinalizer[0] == 1 and valueSinalizer[3] == 1
                if logicOperand[0] == "and":
                    for row in tableToUse.tableContent:
                        if (self.operatorsDict[comparations[0]](attributesToCompare[0], row[tableToUse.collumnNames[attributesToCompare[1]]]) and self.operatorsDict[comparations[1]](row[tableToUse.collumnNames[attributesToCompare[2]]], attributesToCompare[3])):
                            filteredTable.append(row)
                elif logicOperand[0] == "or":
                    for row in tableToUse.tableContent:
                        if (self.operatorsDict[comparations[0]](attributesToCompare[0], row[tableToUse.collumnNames[attributesToCompare[1]]]) or self.operatorsDict[comparations[1]](row[tableToUse.collumnNames[attributesToCompare[2]]], attributesToCompare[3])):
                            filteredTable.append(row)
        elif qntOfValueAttributes == 1:
            if logicOperand == []:
                if valueSinalizer[0] == 1:
                    for row in tableToUse.tableContent:
                        if self.operatorsDict[comparations[0]](attributesToCompare[0], row[tableToUse.collumnNames[attributesToCompare[1]]]):
                            filteredTable.append(row)
                else: # valueSinalizer[1] == 1
                    for row in tableToUse.tableContent:
                        if self.operatorsDict[comparations[0]](row[tableToUse.collumnNames[attributesToCompare[0]]], attributesToCompare[1]):
                            filteredTable.append(row)
        elif qntOfValueAttributes == 0:
            if logicOperand == []:
                for row in tableToUse.tableContent:
                    if self.operatorsDict[comparations[0]](row[tableToUse.collumnNames[attributesToCompare[0]]], row[tableToUse.collumnNames[attributesToCompare[1]]]):
                        filteredTable.append(row)
            elif logicOperand[0] == "and":
                for row in tableToUse.tableContent:
                    if (self.operatorsDict[comparations[0]](row[tableToUse.collumnNames[attributesToCompare[0]]], row[tableToUse.collumnNames[attributesToCompare[1]]]) and self.operatorsDict[comparations[1]](row[tableToUse.collumnNames[attributesToCompare[2]]], row[tableToUse.collumnNames[attributesToCompare[3]]])):
                        filteredTable.append(row)
            elif logicOperand[0] == "or":
                for row in tableToUse.tableContent:
                    if (self.operatorsDict[comparations[0]](row[tableToUse.collumnNames[attributesToCompare[0]]], row[tableToUse.collumnNames[attributesToCompare[1]]]) or self.operatorsDict[comparations[1]](row[tableToUse.collumnNames[attributesToCompare[2]]], row[tableToUse.collumnNames[attributesToCompare[3]]])):
                        filteredTable.append(row)
        else:
            print("Couldn't compare attributes.\n")

        return filteredTable

    def joinTwoTables(self, tablesToJoin, joinEquality):
        return