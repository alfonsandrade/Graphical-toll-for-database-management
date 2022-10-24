import sys
import os
import re

from Table import Table

class Database:
    def __init__(self, dirPath : str):
        self.tables = {}

        for root, direc, file in os.walk(dirPath):
            filePath = os.path.join(root, direc, file)

            if filePath.endswith(".csv"):
                newTable = Table(file, filePath)
                self.tables.append(newTable)

    def searchLoop(self):
        query = "nop"
        whatToSelect = {}
        selectFrom = {}
        where = {}
        order_by = {}

        # Mainloop for searching in database
        while query != "quit;":
            query = input()
            query = query.split(' ')

            result = self.queryTreatment(query)

            whatToSelect = result[0]
            print(whatToSelect )
            selectFrom   = result[1]
            print(selectFrom)
            where        = result[2]
            print(where)
            order_by     = result[3]
            print(order_by)

            if whatToSelect == {}:
                continue
            elif whatToSelect[0] == "*":
                if where == {} and order_by == {}:
                    # Select * from chosen
                elif where == {}:
                    # Select * from chosen order by chum
                elif order_by == {}:
                    # Select * from chosen where apoaisnvaosid
                else:
                    # Select * from chosen where paosdvaso order by oasivaosi
            else:
                if where == {} and order_by == {}:
                    # Select * from chosen
                elif where == {}:
                    # Select * from chosen order by chum
                elif order_by == {}:
                    # Select * from chosen where apoaisnvaosid
                else:
                    # Select * from chosen where paosdvaso order by oasivaosi





    def queryTreatment(self, query):
        whatToSelect = {}
        selectFrom = {}
        where = {}
        order_by = {}
        
        iterator = 0
        while iterator < len(query):
            if query[iterator] == "select":
                selecWhat = iterator + 1
                while query[selecWhat] != "from":
                    whatToSelect.append(query[selecWhat])
                    selecWhat += 1

                iterator = selecWhat
            
            if query[iterator] == "from":
                fromWhat = iterator + 1
                while query[fromWhat] != "where" or query[fromWhat] != ";":
                    selectFrom.append(query[fromWhat])
                    fromWhat += 1

                iterator = fromWhat

            if query[iterator] == "where":
                filters = iterator + 1
                while query[filters] != "order" or query[filters] != ";":
                    where.append(query[filters])
                    filters += 1

                iterator = filters

            if query[iterator] == "order":
                ordering = iterator + 2
                while query[ordering] != ";":
                    order_by.append(query[ordering])
                    ordering += 1

                iterator = ordering

            iterator += 1

        return whatToSelect, selectFrom, where, order_by

    def resultingSelect(whatToSelect,selectFrom,where,order_by):