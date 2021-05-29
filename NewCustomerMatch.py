from sqlalchemy import create_engine
import sys
import shutil
from time import strftime,localtime
import Migration as mg
import Currency as cr
import pandas as pd
import xlsxwriter
import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class TR3:
    def __init__(self) -> None:
        self.date = strftime("%d%m%Y%H%M%S", localtime())

    def SecondLevelMigration(self,SourceFolderPath:str,DestinationFolderPath:str) -> None:
        self.SourceFolderPath= SourceFolderPath
        self.DestinationFolderPath= DestinationFolderPath
        self.database_connection()
        self.database_NewMatchCustomer()
        # self.movefiles()
        self.con.close

    def movefiles(self) ->None:
        shutil.move(self.SourceFolderPath+'customers.csv', self.DestinationFolderPath + '/customers_'+self.date +'.csv')
        shutil.move(self.SourceFolderPath+'transactions.csv', self.DestinationFolderPath + '/transactions_'+self.date +'.csv')
        shutil.move(self.SourceFolderPath+'Currency.xml', self.DestinationFolderPath + '/Currency_'+self.date +'.xml')

    def database_connection(self) ->None:
        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root",pw="diplo@123",db="work"))
        self.con = engine.connect()
    
    def database_NewMatchCustomer(self) -> None:
        try:
            self.con.execute("drop table NewCustomerMatch")
            self.con.execute("CREATE TABLE NewCustomerMatch AS SELECT customermatch.ID AS customer_id,customermatch.LastName AS customer_last_name,customermatch.FirstName AS customer_first_name,customermatch.TransactionID AS transaction_id,CASE WHEN customermatch.currency_id = currencytable.id THEN customermatch.amount / currencytable.rate ELSE customermatch.amount END AS amount, CASE WHEN customermatch.currency_id = currencytable.id THEN currencytable.currency ELSE customermatch.currency_id END AS currency FROM customermatch LEFT OUTER JOIN currencytable ON customermatch.currency_id = currencytable.id;")
        except:
            self.con.execute("CREATE TABLE NewCustomerMatch AS SELECT customermatch.ID AS customer_id,customermatch.LastName AS customer_last_name,customermatch.FirstName AS customer_first_name,customermatch.TransactionID AS transaction_id,CASE WHEN customermatch.currency_id = currencytable.id THEN customermatch.amount / currencytable.rate ELSE customermatch.amount END AS amount, CASE WHEN customermatch.currency_id = currencytable.id THEN currencytable.currency ELSE customermatch.currency_id END AS currency FROM customermatch LEFT OUTER JOIN currencytable ON customermatch.currency_id = currencytable.id;")


class TR4:

    def database_connection1(self) ->None:
        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root",pw="diplo@123",db="work"))
        self.con = engine.connect()
        self.UnsupportedCustomer()
        self.BadCustomer()
        self.RiskyCustomer()

    def UnsupportedCustomer(self):  
        self.df = pd.read_sql("SELECT * FROM NewCustomerMatch WHERE currency REGEXP '[0-9]'", con = self.con)
        # data = self.df
        # print(data)
        # data.to_excel("Required.xlsx", sheet_name='UnsupportedCustomer', index=False)
        
    def BadCustomer(self):
        self.df_1 = pd.read_sql("SELECT * FROM NewCustomerMatch WHERE customer_id IS NULL", con = self.con)
        # self.df_1.to_excel("Required.xlsx", sheet_name='TransactionsWithBadCustomerID', index=False)

    def RiskyCustomer(self):
        self.df_2 = pd.read_sql("SELECT * FROM WORK.NewCustomerMatch WHERE customer_id IN (SELECT customer_id FROM WORK.NewCustomerMatch GROUP BY customer_id HAVING SUM(amount) > 400000) ", con = self.con)
        # print(self.df_2)
        writer = pd.ExcelWriter('./Demo/DestinationFolder/FinalResults.xlsx')
        self.df_2.to_excel(writer, sheet_name='RiskyCustomer',index=False)
        self.df_1.to_excel(writer, sheet_name='TransactionsWithBadCustomerID', index=False)
        self.df.to_excel(writer, sheet_name='UnsupportedCurrency', index=False)
        
        writer.save()
        # print(writer)
        if os.path.isfile('./Demo/DestinationFolder/FinalResults.xlsx'):
            print (" File exist " + " name of the file:FinalResults.xlsx " + "location:./Demo/DestinationFolder")
            fromaddr = "hritiksth764@gmail.com"
            # toaddr = "manish.instru@gmail.com"
            toaddr = input("Receiver's mail id:")
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = " BRD_CC_Fraud_Detection"
            body = "Here are the final results"
            msg.attach(MIMEText(body, 'plain'))
            # open the file to be sent 
            filename = "FinalResults.xlsx"
            attachment = open("./Demo/DestinationFolder/FinalResults.xlsx", "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            # encode into base64
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            # attach the instance 'p' to instance 'msg'
            msg.attach(p)
            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)
            # start TLS for security
            s.starttls()
            # Authentication
            password = input("enter your password")
            s.login(fromaddr, password)
            # Converts the Multipart msg into a string
            text = msg.as_string()
            # sending the mail
            s.sendmail(fromaddr, toaddr, text)
            # terminating the session
            s.quit()
            
        else:
            print ("File not exist")





if __name__ == "__main__":
    #Static Folder Paths
    ejSourceFolderPath = f"./Demo/SourceFolder/"
    ejDestinationFolderPath = f"./Demo/DestinationFolder/"
    try:
        # ejSourceFolderPath = sys.argv[1]
        # ejDestinationFolderPath = sys.argv[2]
        migration= mg.TR1()
        migration.FirstLevelMigration(ejSourceFolderPath,ejDestinationFolderPath)
        currency= cr.Currency()
        currency.FirstLevelMigrationPart2(ejSourceFolderPath,ejDestinationFolderPath)
        newmatch=TR3()
        newmatch.SecondLevelMigration(ejSourceFolderPath,ejDestinationFolderPath)
        newcustomer = TR4()
        newcustomer.database_connection1()
    except IndexError:
        ejSourceFolderPath= input("Enter the Source path of your file: ")
        ejDestinationFolderPath= input("Enter the Destination path of your file: ")
        migration= mg.TR1()
        migration.FirstLevelMigration(ejSourceFolderPath,ejDestinationFolderPath)
        currency= cr.Currency()
        currency.FirstLevelMigrationPart2(ejSourceFolderPath,ejDestinationFolderPath)
        newmatch=TR3()
        newmatch.SecondLevelMigration(ejSourceFolderPath,ejDestinationFolderPath)
        newcustomer = TR4()
        newcustomer.database_connection1()
