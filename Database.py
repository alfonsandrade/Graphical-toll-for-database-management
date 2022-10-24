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
        selectFrom = []
        where = []
        order_by = []

        # Mainloop for searching in database
        while query != "quit;":
            query = input()
            query = query.split(' ')

            print(query)

            isQueryOk = self.verifyPointCommaInTheEnd(query)
            if isQueryOk == False:
                continue

            result = self.queryTreatment(query)

            whatToSelect = result[0]
            print(whatToSelect )
            selectFrom   = result[1]
            print(selectFrom)
            where        = result[2]
            print(where)
            order_by     = result[3]
            print(order_by)

            isQueryOk = self.isQuerySintaxOk(whatToSelect, selectFrom, where, order_by)
            if isQueryOk == False:
                print("There is an error in your SQL sintax.")
                continue

            # if whatToSelect == []:
            #     continue
            # elif whatToSelect[0] == "*":
            #     if where == [] and order_by == []:
            #         # Select * from chosen
            #     elif where == []:
            #         # Select * from chosen order by chum
            #     elif order_by == []:
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


    def verifyPointCommaInTheEnd(self, query):
        if ';' in query[len(query) - 1]:
            return True
        else:
            print("There is an error in your SQL sintax. Expected ';'.")
            return False


    def queryTreatment(self, query):
        whatToSelect = []
        selectFrom = []
        where = []
        order_by = []
        
        query[len(query) - 1] = query[len(query) - 1][:-1]

        iterator  = 0
        # Used to sinalize what part of the query the iterator is currently running
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
        for table in self.tables:
            if table.tableName == selectFrom[0]:
                usedTable = table
                sintaxOk  = True

        # Checks rathen attrbutes do exist in the table
        if whatToSelect[0] != '*' and sintaxOk == True:
            for attribute in whatToSelect:
                if attribute not in usedTable.collumnNames:
                    sintaxOk = False

        if order_by != [] and order_by[0] not in whatToSelect:
            sintaxOk = False

        return sintaxOk


    def resultingSelect(whatToSelect, selectFrom, where, order_by):

        return 0