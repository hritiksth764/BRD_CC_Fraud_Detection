import sys
from sqlalchemy import create_engine
import xml.etree.ElementTree as ET
import pandas as pd
from time import strftime,localtime
import shutil

class Currency:
    def __init__(self) -> None:
        pass
    
    def FirstLevelMigrationPart2(self,SourceFolderPath:str,DestinationFolderPath:str) -> None:
        self.SourceFolderPath= SourceFolderPath
        self.DestinationFolderPath= DestinationFolderPath
        self.parsexml()
        self.xmltodb()
        self.database_insertion()
        self.con.close
        #shutil.move(self.SourceFolderPath+'/Currency.xml', self.DestinationFolderPath + '/Currency_'+self.date +'.xml')

    def parsexml(self) -> None:
        tree = ET.parse(self.SourceFolderPath+'/Currency.xml')
        root = tree.getroot()
        self.currencytable={}
        namespaces = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
        for cube in root.findall('.//ex:Cube[@currency]', namespaces=namespaces):
            curr_name = cube.attrib['currency']
            curr_rate = float(cube.attrib['rate'])
            self.currencytable[curr_name]=curr_rate
    
    def xmltodb(self) -> None: 
        self.currency_df=pd.DataFrame(self.currencytable.items(),columns=['currency','rate'])
        self.currency_df.reset_index(inplace=True)
        self.currency_df = self.currency_df.rename(columns = {'index':'id'})

    def database_connection(self) ->None:
        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root",pw="diplo@123",db="work"))
        self.con = engine.connect()
    
    def database_insertion(self) -> None:
        self.database_connection()
        self.currency_df.to_sql('currencytable', con = self.con, if_exists = 'replace', index=False)

'''
if __name__ == "__main__":
    #Static Folder Paths
    ejSourceFolderPath = f"./Demo/Source/"
    ejDestinationFolderPath = f"./Demo/Destination/"
    try:
        #ejSourceFolderPath = sys.argv[1]
        #ejDestinationFolderPath = sys.argv[2]
        currency= Currency()
        currency.FirstLevelMigrationPart2(ejSourceFolderPath,ejDestinationFolderPath)
    except IndexError:
        ejSourceFolderPath= input("Enter the Source path of your file: ")
        ejDestinationFolderPath= input("Enter the Destination path of your file: ")
        currency= Currency()
        currency.FirstLevelMigrationPart2(ejSourceFolderPath,ejDestinationFolderPath)
'''