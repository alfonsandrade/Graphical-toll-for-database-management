import sys
import os
import re

from Table import Table

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

    def searchLoop(self):
        query = "nop"
        whatToSelect = []
        selectFrom   = []
        where        = []
        order_by     = []

        # Mainloop for searching in database
        while query[0] != "quit;":
            print("> ")
            query = input()
            query = query.split(' ')

            if query[0] == "quit;":
                break

            print(query)

            isQueryOk = self.verifyPointCommaInTheEnd(query)
            if isQueryOk == False:
                continue

            result = self.queryTreatment(query)

            whatToSelect = result[0]
            selectFrom   = result[1]
            where        = result[2]
            order_by     = result[3]
            print(whatToSelect )
            print(selectFrom)
            print(where)
            print(order_by)

            isQueryOk = self.isQuerySintaxOk(whatToSelect, selectFrom, where, order_by)
            if isQueryOk == False:
                continue

            if whatToSelect[0] == "*":
                if where == [] and order_by == []:
                    # Select * from chosen
                    self.selectAllFrom(selectFrom)
            #     elif where == []:
            #         # Select * from chosen order by chum
                # elif order_by == []:
            #         # Select * from chosen where apoaisnvaosid
            #     else:
            #         # Select * from chosen where paosdvaso order by oasivaosi
            # else:
            #     if where == [] and order_by == []:
            #         # Select * from chosen
            #     elif where == []:
            #         # Select * from chosen order by chum
            #     elif order_by == []:
            #         # Select * from chosen where apoaisnvaosid
            #     else:
            #         # Select * from chosen where paosdvaso order by oasivaosi

        return


    def verifyPointCommaInTheEnd(self, query) -> bool:
        if ';' in query[len(query) - 1]:
            return True
        else:
            print("There is an error in your SQL sintax. Expected ';'.")
            return False


    # Devides the query into four arrays, the ones declared down below
    def queryTreatment(self, query):
        whatToSelect = []
        selectFrom   = []
        where        = []
        order_by     = []

        # Removes ; from the last word or removes it completely if it's only a ;
        if len(query[len(query) - 1]) > 1:
            query[len(query) - 1] = query[len(query) - 1][:-1]
        else:
            query = query[:-1]

        iterator  = 0

        # Semaphore used to sinalize what part of the query the iterator is currently running on
        # 1 - select
        # 2 - from
        # 3 - where
        # 4 - order by
        semaphore = 0 
        while iterator < len(query):
            if query[iterator].lower() == "select":
                semaphore = 1
            elif query[iterator].lower() == "from":
                semaphore = 2
            elif query[iterator].lower() == "where":
                semaphore = 3
            elif query[iterator].lower() == "order":
                semaphore = 4
                iterator += 1 # To jump the "by" word
            else:
                if semaphore == 1:
                    whatToSelect.append(query[iterator])
                elif semaphore == 2:
                    selectFrom.append(query[iterator])
                elif semaphore == 3:
                    where.append(query[iterator])
                elif semaphore == 4:
                    order_by.append(query[iterator])
                else:
                    pass

            iterator += 1

        return whatToSelect, selectFrom, where, order_by

    def isQuerySintaxOk(self, whatToSelect, selectFrom, where, order_by):
        sintaxOk = False
        
        # Finds table to be used
        if whatToSelect == []:
            print("There is nothing to select.")
        elif selectFrom == []:
            print("No table to select from.")
        else:
            for table in self.tables:
                if table.tableName == selectFrom[0]:
                    usedTable = table
                    sintaxOk  = True
            # Relations table was not found
            if sintaxOk == False:
                print("Error: no table called " + selectFrom[0] + " was found.")


            # Checks rathen attrbutes do exist in the table
            if whatToSelect[0] != '*' and sintaxOk == True:
                for attribute in whatToSelect:
                    if attribute not in usedTable.collumnNames:
                        print("Error: there is no " + attribute + " in " + usedTable.tableName)
                        sintaxOk = False

            if order_by != [] and order_by[0] not in whatToSelect:
                print("There is an error in your SQL sintax.")
                sintaxOk = False

        return sintaxOk

    ########################## QUERY ALGORYTHMS ###############################

    # select * from something
    def selectAllFrom(self, selectFrom):
        for table in self.tables:
            if table.tableName == selectFrom[0]:
                tableToUse = table

        print("/           " + tableToUse.tableName + "              /")
        print(tableToUse.collumnNames)
        for line in tableToUse.tableContent:
            print(line)

        print("\n")

        return

    def selectAllFromWhere(self, selectFrom, where):
        opperand            = ""
        comparations        = []
        attributesToCompare = []

        # for word in where:

        
        for table in self.tables:
            if table.tableName == selectFrom[0]:
                tableToUse = table

        print("/           " + tableToUse.tableName + "              /")
        print(tableToUse.collumnNames)

        return