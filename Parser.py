import sys
import os

class Parser:
    def __init__(self):
        pass

    @staticmethod
    def verifyPointCommaInTheEnd(query) -> bool:
        if ';' in query[-1]:
            return True
        print("There is an error in your SQL sintax. Expected ';'.")
        return False


    # Devides the query into six arrays, the ones declared down below
    @staticmethod
    def queryTreatment(query):
        whatToSelect    = []
        selectFrom      = []
        where           = []
        order_by        = []
        tablesToJoin    = []
        joinEquality    = []
        joinEqlFiltered = []

        # Removes ; from the last word or removes it completely if it's only a ;
        if len(query[-1]) > 1:
            query[-1] = query[-1][-1]
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

        # Finding joins with join argument in from statement
        iterator = 0
        for iterator in range(len(selectFrom)):
            if selectFrom[iterator] == 'inner' and selectFrom[iterator + 1] == 'join':
                tablesToJoin.append(selectFrom[iterator - 1])
                tablesToJoin.append(selectFrom[iterator + 2])
                iterator += 2 # Might have to change the qnt of jumps
            elif selectFrom[iterator] == 'join':
                tablesToJoin.append(selectFrom[iterator - 1])
                tablesToJoin.append(selectFrom[iterator + 1])
                iterator += 1
            elif selectFrom[iterator] == 'on' or selectFrom[iterator] == 'using':
                joinEquality.append(selectFrom[iterator + 1].split('.'))
                joinEquality.append(selectFrom[iterator + 3].split('.'))
                iterator += 3

            if iterator >= len(selectFrom):
                break

        # Join attributes
        if joinEquality != []:
            for row in joinEquality:
                joinEqlFiltered.append(row[len(row) - 1])

        # Finding implicit joins in where statement
        if tablesToJoin == []:
            iterator = 0
            aux      = []
            for iterator in range(len(where)):
                if where[iterator] == '=':
                    # Comparison between tables attributes
                    if '.' in where[iterator - 1] and '.' in where[iterator + 1]:
                        aux.append(where[iterator - 1].split('.')) # Splits words into table name and attribute name
                        aux.append(where[iterator + 1].split('.'))
                        
                        if len(where) < 4: # If this is the only clausule in where
                            where = []
                            break
                        elif iterator < 3: # If this is the first clausule
                            where = where[(iterator + 3):] # Removes it from where
                            break
                        elif iterator > 3: # If this is the second clausule
                            where = where[:(iterator - 3)]
                            break
                        
                        if iterator >= len(where):
                            break # Double checking to avoid seg fault 

            iterator = 0
            if aux != []:
                # Puts table names in tablesToJoin and attributes in joinEqlFiltered
                for row in aux:
                    joinEqlFiltered.append(row[1])
                    tablesToJoin.append(row[0])

        # Treating whatToSelect for when there is a join
        if tablesToJoin != []:
            iterator = 0
            while iterator < len(whatToSelect):
                if '.' in whatToSelect[iterator]:
                    whatToSelect[iterator] = whatToSelect[iterator].split('.')
                
                iterator += 1


        return whatToSelect, selectFrom, where, order_by, tablesToJoin, joinEqlFiltered

    @staticmethod
    def isQuerySyntaxOk(relations, whatToSelect, selectFrom, where, order_by, tablesToJoin, joinEquality):
        syntaxOk   = False
        usedTables = []

        # Finds table to be used
        if whatToSelect == []:
            print("There is nothing to select.\n")
        elif selectFrom == []:
            print("No table to select from.\n")
        elif len(selectFrom) == 1: # For simple queries
            for table in relations:
                if table.tableName == selectFrom[0]:
                    usedTables.append(table)
                    syntaxOk  = True
            # Relations table was not found
            if syntaxOk is False:
                print("Error: no table called " + selectFrom[0] + " was found.\n")
        else: # Queries with join
            qntOfExistingTables = 0
            for table in relations:
                for joinTableName in tablesToJoin:
                    if table.tableName == joinTableName:
                        usedTables.append(table)
                        qntOfExistingTables += 1

            if qntOfExistingTables == len(tablesToJoin):
                syntaxOk = True
            else:
                print((len(tablesToJoin) - qntOfExistingTables), " tables in join statement don't exist")

        # Checks wether attributes do exist in the table
        if syntaxOk is True and tablesToJoin == [] and whatToSelect[0] != '*':
            for attribute in whatToSelect:
                for table in usedTables:
                    if attribute not in table.collumnNames:
                        print("Error: there is no " + attribute + " in " + table.tableName + "\n")
                        syntaxOk = False

        # Checks wether order_by attributes do exist in the table
        if syntaxOk is True and order_by != []:
            for attribute in order_by:
                for table in usedTables:
                    if attribute not in table.collumnNames:
                        print("Error: there is no " + attribute + " in " + table.tableName + "\n")
                        syntaxOk = False

        # Checks wether all tables to join are declared in From statement
        if syntaxOk is True and tablesToJoin != []:
            for tableName in tablesToJoin:
                if tableName not in selectFrom:
                    print(tableName + " is not declared in From statement.")
                    syntaxOk = False

        # Checks wether join attributes do exist in the tables to join
        if syntaxOk is True and joinEquality != []:
            iterator = 0
            for iterator in range(len(joinEquality)):
                if joinEquality[iterator] not in usedTables[iterator].collumnNames:
                    print("The attribute " + joinEquality[iterator] + " doesn't exist in " + usedTables[iterator].tableName + " relation.")
                    syntaxOk = False

        # Checks if order by attributes are in what to select
        if syntaxOk is True and order_by != [] and whatToSelect[0] != '*' and order_by[0] not in whatToSelect:
            print("There is an error in your SQL sintax.\n")
            syntaxOk = False

        return syntaxOk