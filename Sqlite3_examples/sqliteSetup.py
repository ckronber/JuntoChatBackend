import sqlite3 as sq3

class dbConnection():
    def __init__(self,dbName):
        print(sq3.version)
        print(sq3.sqlite_version)

        fullPath = "Sqlite3_examples/"+dbName + ".db"
        con = sq3.connect(fullPath)
        self.con = con
        cur = con.cursor()
        self.cur = cur

    def createDB(self,dbName = "default"):
        fullPath = "Sqlite3_examples/"+dbName + ".db"
        self.dbName = fullPath
        con = sq3.connect(self.dbName)
        self.con = con
        cur = con.cursor()
        self.cur = cur

    def CreateTable(self,*rows):
        # Create table
        self.length = 4
        tableVals = ''

        for i,row in enumerate(rows):
            if(i < len(rows)-1):
                tableVals += row + ','
            else:
                tableVals += row

        self.cur.execute(f"CREATE TABLE stocks ({tableVals})")

    def InsertRow(self,*items):
        # Insert a row of data
        self.length = 4
        tableVals = ''

        for i,row in enumerate(items):
            if(i < len(items)-1):
                tableVals += row + ','
            else:
                tableVals += row

        if(self.length == len(items)):
            self.cur.execute(f"INSERT INTO stocks VALUES ({tableVals})")

    def sortby(self):
        for row in self.cur.execute(f'SELECT * FROM stocks ORDER BY Price'):
            print(row)    

    def SaveChanges(self):
        # Save (commit) the changes
        self.con.commit()
        
    def CloseConnection(self):
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.con.close()

firstConnect = dbConnection("testData")
#firstConnect.createDB("testData")
#firstConnect.CreateTable("Ticker","Price","Amount","Value")
#firstConnect.InsertRow('"BTC"','46000','1','46000*1')
#firstConnect.InsertRow('"ETH"','3400','6','3400*6')
#firstConnect.SaveChanges()
#firstConnect.CloseConnection()
#firstConnect.InsertRow('"MATIC"','1.32','2285.2','1.32*2285.2')
firstConnect.sortby()
firstConnect.SaveChanges()
firstConnect.CloseConnection()