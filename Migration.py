import sys
import io
from sqlalchemy import create_engine
import pandas as pd
import shutil
from time import strftime,localtime


class TR1:
    def __init__(self) -> None:
        pass
    
    def FirstLevelMigration(self,SourceFolderPath:str,DestinationFolderPath:str) -> None:
        self.SourceFolderPath= SourceFolderPath
        self.DestinationFolderPath= DestinationFolderPath
        self.clean_csv()
        self.database_connection()
        self.database_insertion()
        self.database_matchCustomer()
        #shutil.move(self.SourceFolderPath+'/customers.csv', self.DestinationFolderPath + '/customers_'+self.date +'.csv')
        #shutil.move(self.SourceFolderPath+'/transactions.csv', self.DestinationFolderPath + '/transactions_'+self.date +'.csv')
        self.con.close

    def clean_csv(self) ->  None:
        self.customerColumn = ['ID', 'LastName', 'FirstName']
        self.transactionColumns = ['TransactionID','ID', 'amount', 'currency_id']
        try:
            with open(self.SourceFolderPath + 'customers.csv','r+') as c:
                content=c.read()
                content=content.replace(',','_')
                content=content.replace(';',',')
                try:
                    self.CustomerData = pd.read_csv(io.StringIO(content), header=None, names=self.customerColumn)
                except:
                    print("Invalid Customer File Structure")
                    sys.exit(1)
        except:
            print("Customer Data File not found on specified path, Please Enter correct folder path")
            sys.exit(1)

        try:
            with open(self.SourceFolderPath + 'transactions.csv','r+') as t:
                content=t.read()
                content=content.replace('"','')
                try:
                    self.TransactionsData = pd.read_csv(io.StringIO(content), header=None, names=self.transactionColumns)
                except:
                    print("Invalid Transactions File Structure")
                    sys.exit(1)

        except:
            print("Transactions Data File not found on specified path, Please Enter correct folder path")
            sys.exit(1)

    def database_connection(self) ->None:
        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root",pw="diplo@123",db="work"))
        self.con = engine.connect()

    def database_insertion(self) -> None:
        self.CustomerData.to_sql('customers', con = self.con, if_exists = 'replace', index = False)
        self.TransactionsData.to_sql('transactions', con = self.con, if_exists = 'replace', index = False)

    def database_matchCustomer(self) -> None:
        try:
            self.con.execute("drop table CustomerMatch")
            self.con.execute("create table CustomerMatch AS select customers.ID, customers.LastName, customers.FirstName, transactions.TransactionID, transactions.amount, transactions.currency_id FROM transactions LEFT OUTER JOIN customers ON(transactions.ID= customers.ID );")
        except:
            self.con.execute("create table CustomerMatch AS select customers.ID, customers.LastName, customers.FirstName, transactions.TransactionID, transactions.amount, transactions.currency_id FROM transactions LEFT OUTER JOIN customers ON(transactions.ID= customers.ID );")

"""
if __name__ == "__main__":
    #Static Folder Paths
    ejSourceFolderPath = f"./Demo/Source/"
    ejDestinationFolderPath = f"./Demo/Destination/"
    try:
        #ejSourceFolderPath = sys.argv[1]
        #ejDestinationFolderPath = sys.argv[2]
        migration= FirstLevelMigration(ejSourceFolderPath,ejDestinationFolderPath)
        migration.process_data()
    except IndexError:
        ejSourceFolderPath= input("Enter the Source path of your file: ")
        ejDestinationFolderPath= input("Enter the Destination path of your file: ")
        migration= FirstLevelMigration(ejSourceFolderPath,ejDestinationFolderPath)
        migration.process_data()
"""

