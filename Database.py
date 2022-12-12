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

        print("\nWhere and Order By parameters are only applied to the inner table, failing if you consider the outer one for the conditions.\nThe query will accept the terms >on< or >using< for join.")
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
                    self.selectAllFrom(selectFrom, tablesToJoin, joinEquality)
                elif where == []:
                    # Select * from chosen order by chum
                    self.selectAllFromOrderBy(selectFrom, order_by, tablesToJoin, joinEquality)
                elif order_by == []:
                    # Select * from chosen where lalos < ligos
                    self.selectAllFromWhere(selectFrom, where, tablesToJoin, joinEquality)
                else:
                    # Select * from chosen where paosdvaso order by oasivaosi
                    self.selectAllFromWhereOrderBy(selectFrom, where, order_by, tablesToJoin, joinEquality)
            else:
                if where == [] and order_by == []:
                    self.selectSomethingFrom(whatToSelect, selectFrom, tablesToJoin, joinEquality)
                elif where == []:
                    self.selectSomethingFromOrderBy(whatToSelect, selectFrom, order_by, tablesToJoin, joinEquality)
                elif order_by == []:
                    self.selectSomethingFromWhere(whatToSelect, selectFrom, where, tablesToJoin, joinEquality)
                else:
                    self.selectSomethingFromWhereOrderBy(whatToSelect, selectFrom, where, order_by, tablesToJoin, joinEquality)

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
        else:
            for table in self.tables:
                if table.tableName in tablesToJoin:
                    tablesToUse.append(table)

            tableToPrint = self.nestedLoopJoinTwoTables(tablesToUse[0].tableContent,
                                                        tablesToUse[1].tableContent,
                                                        tablesToUse[0].collumnNames[joinEquality[0]],
                                                        tablesToUse[1].collumnNames[joinEquality[1]])

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

        return

    # select * from something order by something
    def selectAllFromOrderBy(self, selectFrom, order_by, tablesToJoin, joinEquality):
        tablesToUse  = []
        tableToPrint = []

        if tablesToJoin == []:     
            for table in self.tables:
                if table.tableName == selectFrom[0]:
                    tablesToUse.append(table)
            
            orderedTable = self.mergeSortByCollumn(tablesToUse[0].tableContent, 0, len(tablesToUse[0].tableContent)-1, tablesToUse[0].collumnNames[order_by[0]])
        
        else:
            for table in self.tables:
                if table.tableName in tablesToJoin:
                    tablesToUse.append(table)
            
            tableToPrint = self.nestedLoopJoinTwoTables(tablesToUse[0].tableContent,
                                                        tablesToUse[1].tableContent,
                                                        tablesToUse[0].collumnNames[joinEquality[0]],
                                                        tablesToUse[1].collumnNames[joinEquality[1]])
            
            orderedTable = self.mergeSortByCollumn(tableToPrint, 0, len(tableToPrint)-1, tablesToUse[0].collumnNames[order_by[0]])

        if orderedTable != []:
            for table in tablesToUse:
                print("|                " + table.tableName + "                |", end = '')
            print('')
            print("|", end = '')
            for table in tablesToUse:
                for collum in table.collumnNames:
                    print("  "+ collum + "  |", end = '')
            print("")
            for line in orderedTable:
                print(line)

            print("\n")

    # select * from something where something < 78
    def selectAllFromWhere(self, selectFrom, where, tablesToJoin, joinEquality):
        tablesToUse  = []
        tableToPrint = []
        
        if tablesToJoin == []:
            for table in self.tables:
                if table.tableName == selectFrom[0]:
                    tablesToUse.append(table)

            tableToPrint = self.manageWhere(where, tablesToUse[0])

        else:
            for table in self.tables:
                if table.tableName in tablesToJoin:
                    tablesToUse.append(table)
            
            filteredTable1 = self.manageWhere(where, tablesToUse[0])
            # filteredTable2 = self.manageWhere(where, tableToUse[1])
            
            tableToPrint = self.nestedLoopJoinTwoTables(filteredTable1,
                                                        tablesToUse[1].tableContent,
                                                        tablesToUse[0].collumnNames[joinEquality[0]],
                                                        tablesToUse[1].collumnNames[joinEquality[1]])
        
        if tableToPrint != []:
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

        print("\n")

    def selectAllFromWhereOrderBy(self, selectFrom, where, order_by, tablesToJoin, joinEquality):
        tablesToUse  = []
        tableToPrint = []
        
        if tablesToJoin == []:
            for table in self.tables:
                if table.tableName == selectFrom[0]:
                    tableToUse = table

            tableToPrint = self.manageWhere(where, tableToUse)
            tableToPrint = self.mergeSortByCollumn(tableToPrint, 0, len(tableToPrint)-1, tableToUse.collumnNames[order_by[0]])
        
            if tableToPrint != []:
                print("|                " + tableToUse.tableName + "                |")
                print("|", end = '')
                for line in tableToUse.collumnNames:
                    print("  "+line + "  |", end = '')
                print("")
                for line in tableToPrint:
                    print(line)
            else:
                print("This relation is empty.")
        
        else:
            for table in self.tables:
                if table.tableName in tablesToJoin:
                    tablesToUse.append(table)

            filteredTable1 = self.manageWhere(where, tablesToUse[0])
            # filteredTable2 = self.manageWhere(where, tableToUse[1])
            
            tableToPrint = self.nestedLoopJoinTwoTables(filteredTable1,
                                                        tablesToUse[1].tableContent,
                                                        tablesToUse[0].collumnNames[joinEquality[0]],
                                                        tablesToUse[1].collumnNames[joinEquality[1]])
            
            orderedTable = self.mergeSortByCollumn(tableToPrint, 0, len(tableToPrint)-1, tablesToUse[0].collumnNames[order_by[0]])

            if orderedTable != []:
                for table in tablesToUse:
                    print("|                " + table.tableName + "                |", end = '')
                print('')
                print("|", end = '')
                for table in tablesToUse:
                    for collum in table.collumnNames:
                        print("  "+ collum + "  |", end = '')
                print("")
                for line in orderedTable:
                    print(line)

                print("\n")

    ################################################################################
    ########################## QUERY ALGORITHMS WITHOUT * ##########################
    ################################################################################

    def selectSomethingFrom(self, whatToSelect, selectFrom, tablesToJoin, joinEquality):
        tablesToUse  = []
        tableToPrint = []

        if tablesToJoin == []:
            for table in self.tables:
                if table.tableName == selectFrom[0]:
                    tablesToUse.append(table)
                    tableToPrint = table.tableContent

            print("|                " + tablesToUse[0].tableName + "                |")
            print("|", end = '')

            for attribute in whatToSelect:
                print("  "+ attribute + "  |", end = '')
            print("")

            for line in tablesToUse[0].tableContent:
                print('|',  end = '')
                for attribute in whatToSelect:
                    print("  ", end = "")
                    print(line[tablesToUse[0].collumnNames[attribute]], end = "")
                    print("  |", end = '')
                print('')

            print("\n")
        else: # If there is a join
            for table in self.tables:
                if table.tableName in tablesToJoin:
                    tablesToUse.append(table)

            tableToPrint = self.nestedLoopJoinTwoTables(tablesToUse[0].tableContent,
                                                        tablesToUse[1].tableContent,
                                                        tablesToUse[0].collumnNames[joinEquality[0]],
                                                        tablesToUse[1].collumnNames[joinEquality[1]])

            for table in tablesToUse:
                print("|                " + table.tableName + "                |", end = '')
            print('')
            print("|", end = '')
            for attribute in whatToSelect:
                print("  "+ attribute[1] + "  |", end = '')
            print("")
            rowSelec = []
            for line in tableToPrint:
                print('|',  end = '')
                for rowSelec in whatToSelect:
                    tablitos = self.returnTable(rowSelec[0])
                    print("  ", end = "")
                    if tablitos.tableName == tablesToUse[0].tableName:
                        print(line[tablitos.collumnNames[rowSelec[1]]], end = "")
                    else:
                        print(line[tablitos.collumnNames[rowSelec[1]] + len(tablesToUse[0].collumnNames)], end = "")
                    print("  |", end = '')
                print('')

            print("\n")

        return

    def selectSomethingFromOrderBy(self, whatToSelect, selectFrom, order_by, tablesToJoin, joinEquality):
        tablesToUse  = []
        tableToPrint = []

        if tablesToJoin == []:
            for table in self.tables:
                if table.tableName == selectFrom[0]:
                    tablesToUse.append(table)
                    tableToPrint = table.tableContent

            orderedTable = self.mergeSortByCollumn(tablesToUse[0].tableContent, 0, len(tablesToUse[0].tableContent)-1, tablesToUse[0].collumnNames[order_by[0]])

            print("|                " + tablesToUse[0].tableName + "                |")
            print("|", end = '')

            for attribute in whatToSelect:
                print("  "+ attribute + "  |", end = '')
            print("")

            for line in orderedTable:
                print('|',  end = '')
                for attribute in whatToSelect:
                    print("  ", end = "")
                    print(line[tablesToUse[0].collumnNames[attribute]], end = "")
                    print("  |", end = '')
                print('')

            print("\n")
        else: # If there is a join
            for table in self.tables:
                if table.tableName in tablesToJoin:
                    tablesToUse.append(table)

            tableToPrint = self.nestedLoopJoinTwoTables(tablesToUse[0].tableContent,
                                                        tablesToUse[1].tableContent,
                                                        tablesToUse[0].collumnNames[joinEquality[0]],
                                                        tablesToUse[1].collumnNames[joinEquality[1]])

            orderedTable = self.mergeSortByCollumn(tableToPrint, 0, len(tableToPrint)-1, tablesToUse[0].collumnNames[order_by[0]])

            for table in tablesToUse:
                print("|                " + table.tableName + "                |", end = '')
            print('')
            print("|", end = '')
            for attribute in whatToSelect:
                print("  "+ attribute[1] + "  |", end = '')
            print("")
            rowSelec = []
            for line in orderedTable:
                print('|',  end = '')
                for rowSelec in whatToSelect:
                    tablitos = self.returnTable(rowSelec[0])
                    print("  ", end = "")
                    if tablitos.tableName == tablesToUse[0].tableName:
                        print(line[tablitos.collumnNames[rowSelec[1]]], end = "")
                    else:
                        print(line[tablitos.collumnNames[rowSelec[1]] + len(tablesToUse[0].collumnNames)], end = "")
                    print("  |", end = '')
                print('')

            print("\n")

        return

    def selectSomethingFromWhere(self, whatToSelect, selectFrom, where, tablesToJoin, joinEquality):
        tablesToUse  = []
        tableToPrint = []

        if tablesToJoin == []:
            for table in self.tables:
                if table.tableName == selectFrom[0]:
                    tablesToUse.append(table)

            tableToPrint = self.manageWhere(where, tablesToUse[0])

            print("|                " + tablesToUse[0].tableName + "                |")
            print("|", end = '')

            for attribute in whatToSelect:
                print("  "+ attribute + "  |", end = '')
            print("")

            for line in tablesToUse[0].tableContent:
                print('|',  end = '')
                for attribute in whatToSelect:
                    print("  ", end = "")
                    print(line[tablesToUse[0].collumnNames[attribute]], end = "")
                    print("  |", end = '')
                print('')

            print("\n")
        else: # If there is a join
            for table in self.tables:
                if table.tableName in tablesToJoin:
                    tablesToUse.append(table)

            filteredTable1 = self.manageWhere(where, tablesToUse[0])

            tableToPrint = self.nestedLoopJoinTwoTables(filteredTable1,
                                                        tablesToUse[1].tableContent,
                                                        tablesToUse[0].collumnNames[joinEquality[0]],
                                                        tablesToUse[1].collumnNames[joinEquality[1]])

            for table in tablesToUse:
                print("|                " + table.tableName + "                |", end = '')
            print('')
            print("|", end = '')
            for attribute in whatToSelect:
                print("  "+ attribute[1] + "  |", end = '')
            print("")
            rowSelec = []
            for line in tableToPrint:
                print('|',  end = '')
                for rowSelec in whatToSelect:
                    tablitos = self.returnTable(rowSelec[0])
                    print("  ", end = "")
                    if tablitos.tableName == tablesToUse[0].tableName:
                        print(line[tablitos.collumnNames[rowSelec[1]]], end = "")
                    else:
                        print(line[tablitos.collumnNames[rowSelec[1]] + len(tablesToUse[0].collumnNames)], end = "")
                    print("  |", end = '')
                print('')

            print("\n")

        return

    def selectSomethingFromWhereOrderBy(self, whatToSelect, selectFrom, where, order_by, tablesToJoin, joinEquality):
        tablesToUse  = []
        tableToPrint = []

        if tablesToJoin == []:
            for table in self.tables:
                if table.tableName == selectFrom[0]:
                    tablesToUse.append(table)

            tableToPrint = self.manageWhere(where, tablesToUse[0])
            tableToPrint = self.mergeSortByCollumn(tableToPrint, 0, len(tableToPrint)-1, tablesToUse[0].collumnNames[order_by[0]])

            print("|                " + tablesToUse[0].tableName + "                |")
            print("|", end = '')

            for attribute in whatToSelect:
                print("  "+ attribute + "  |", end = '')
            print("")

            for line in tablesToUse[0].tableContent:
                print('|',  end = '')
                for attribute in whatToSelect:
                    print("  ", end = "")
                    print(line[tablesToUse[0].collumnNames[attribute]], end = "")
                    print("  |", end = '')
                print('')

            print("\n")
        else: # If there is a join
            for table in self.tables:
                if table.tableName in tablesToJoin:
                    tablesToUse.append(table)

            filteredTable1 = self.manageWhere(where, tablesToUse[0])

            tableToPrint = self.nestedLoopJoinTwoTables(filteredTable1,
                                                        tablesToUse[1].tableContent,
                                                        tablesToUse[0].collumnNames[joinEquality[0]],
                                                        tablesToUse[1].collumnNames[joinEquality[1]])

            tableToPrint = self.mergeSortByCollumn(tableToPrint, 0, len(tableToPrint)-1, tablesToUse[0].collumnNames[order_by[0]])

            for table in tablesToUse:
                print("|                " + table.tableName + "                |", end = '')
            print('')
            print("|", end = '')
            for attribute in whatToSelect:
                print("  "+ attribute[1] + "  |", end = '')
            print("")
            rowSelec = []
            for line in tableToPrint:
                print('|',  end = '')
                for rowSelec in whatToSelect:
                    tablitos = self.returnTable(rowSelec[0])
                    print("  ", end = "")
                    if tablitos.tableName == tablesToUse[0].tableName:
                        print(line[tablitos.collumnNames[rowSelec[1]]], end = "")
                    else:
                        print(line[tablitos.collumnNames[rowSelec[1]] + len(tablesToUse[0].collumnNames)], end = "")
                    print("  |", end = '')
                print('')

            print("\n")

        return

    ####################################################################
    ################## AUXILIARY FUNCTIONS #############################
    ####################################################################

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

    def manageWhere(self, where, tableToUse: Table):
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
            elif attributesToCompare[iterator] != '':
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

    def nestedLoopJoinTwoTables(self, outerTable, innerTable, outerCol, innerCol):
        joinedRow     = []
        joinedTable   = []
        outerIterator = 0
        innerIterator = 0

        maxRowsOuter = len(outerTable)
        maxRowsInner = len(innerTable)
        while outerIterator < maxRowsOuter:
            while innerIterator < maxRowsInner:
                if outerTable[outerIterator][outerCol] == innerTable[innerIterator][innerCol]:
                    for collumn in outerTable[outerIterator]:
                        joinedRow.append(collumn)
                    for collumn in innerTable[innerIterator]:
                        joinedRow.append(collumn)
                    joinedTable.append(joinedRow)
                    joinedRow = []

                innerIterator += 1
            innerIterator = 0
            outerIterator += 1

        return joinedTable

    def returnTable(self, tableName: str) -> Table:
        for table in self.tables:
            if table.tableName == tableName:
                return table