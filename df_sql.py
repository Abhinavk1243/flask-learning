from datetime import datetime
import mysql.connector as msc 
import pandas as pd

from models import mysl_pool_connection,logger,getconfig
logger=logger()

pool_cnxn=mysl_pool_connection()
mycursor=pool_cnxn.cursor()

def csv_to_table(file_name,table_name):
    """ Method insert a data of csv file in sql table

    Args:
        file_name (str): Name of .csv file
    """

    df=pd.read_csv(f"./files/{file_name}",sep="|")
    
    
    database=getconfig("mysql","database")
    
    cols_1=df.columns
    cols_1=list(cols_1)
    para_len=len(cols_1)
    cols_1=",".join([str(i) for i in cols_1])
    parameters=["%s"]*para_len
    parameters=",".join([str(i) for i in parameters])
    val=[]

    
    for i,row in df.iterrows():
        val.append(tuple(row))
    
    try:   
        sql=f"INSERT INTO {database}.{table_name}({cols_1}) VALUES ({parameters}) "           
        mycursor.executemany(sql,val)
            
        logger.debug(f"csv file : {file_name} is successfully inserted in database table : {table_name} ")
    except Exception as error:
        logger.error(f"Exception arise : {error}")
    
    finally:
        pool_cnxn.commit()

            
def  table_to_csv(table_name,file_name):
    """Metod used to insert sql table into dataframe

    Args:
        table_name (str): name of a table
        file_name (str): name csv file in which the sql table is need to stored

    Returns:
        object: dataframe of sql table
    """

    
    db=getconfig("mysql","database")
    try:
        df=pd.read_sql(con=pool_cnxn, sql=f"SELECT * FROM {db}.{table_name}")
        df.to_csv(f"./files/{file_name}",sep="|",index=False)
        logger.debug(f"data of table : {table_name}  is stored in csv file :{file_name} ")  
    except Exception as error:
        logger.error(f"Exception arise : {error}")
    finally:
        pool_cnxn.close()

        

   
def create_table(file_name,table_name):
    """method used to create table on mysql server of dataframe in csv file 

    Args:
        file_name (str): name of csv file
        table_name (str): name of table want to created
    """
    
    
    df=pd.DataFrame()

    try:
        df=pd.read_csv(f"./files/{file_name}",sep="|")
    except FileExistsError as error:
        logger.error(f"error arise : {error}")
    except Exception as error:
        logger.error(f"Exception arise : {error}")
    
    cols=list(df.columns)

    k=0
    for i,j in df.iterrows():
        if k==0:
            tup=list(j)
            data_type=[]
            for item in tup:
                data_type.append(item)
        break


    table_schema=[]
    k=0
    first=0
    for col in cols:
        if isinstance(data_type[k],int):
            if first ==0:
                table_schema.append(f"{col} int primary key")
            else:
                table_schema.append(f"{col} int")
        elif isinstance(data_type[k],str):
            table_schema.append(f"{col} TEXT")
        elif isinstance(data_type[k],float):
            table_schema.append(f"{col} decimal(6)")
        elif isinstance(data_type[k],datetime):
            table_schema.append(f"{col} datetime(fsp)")
        first=1
        k=k+1

    table_schema=",".join([str(i) for i in table_schema])
    db=getconfig("mysql","database")

    try:
        #print(f"create table test_db.{file_name}({table_schema})")
        sql=f"CREATE TABLE {db}.{table_name}({table_schema})"
        mycursor.execute(sql)
        pool_cnxn.commit()
        logger.debug(f"create table {db}.{table_name}({cols}) ")
    except Exception as error:
        logger.error(f"exception arise : {error}")

    

def checkTableExists(tablename):
    
    
    print(f"SELECT COUNT(*) FROM information_schema.tables \
        WHERE TABLE_SCHEMA = 'web_data' AND TABLE_NAME = '{tablename}' ")
    mycursor.execute(f"SELECT COUNT(*) FROM information_schema.tables \
        WHERE TABLE_SCHEMA = 'web_data' AND TABLE_NAME = '{tablename}' ")
    result=mycursor.fetchone()
    mycursor.close()

    if result[0]== 1:
        return True

    else:
        return False


