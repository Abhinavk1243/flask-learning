import mysql.connector as msc
from mysql.connector import pooling
import logging as lg 
import configparser
import os
def getconfig(section,key):
    """Method use to read the value of key in congfig file i.e .cfg extension file

    Args:
        section (string): section name in cfg file whose value want to read
        key (string): key identification of section whose value want to read

    Returns:
        string: value of corresonding section key
    """
    parser = configparser.ConfigParser()
    parser.read(os.path.join(os.path.expanduser("~"),'config/sqlcred.cfg'))
    return parser.get(section,key)  

def mysl_pool_connection(section):
    """Metod is use to connect database with python 

    Returns:
        connection : myslconnection
    """
    dbconfig={ 
              'host' : getconfig(section,"host"),
              'user' : getconfig(section,"user"),
              'database' : getconfig(section,"database"),
              'password' : getconfig(section,"password"),  
              'auth_plugin': 'mysql_native_password'
            }
    
    cnxn = pooling.MySQLConnectionPool(pool_name = "student",**dbconfig)
    pool_cnxn=cnxn.get_connection()
    return pool_cnxn

def logger():
    logger = lg.getLogger(__name__)
    logger.setLevel(lg.DEBUG)
    formatter = lg.Formatter('%(asctime)s : %(name)s : %(filename)s : %(levelname)s\
                             :%(funcName)s :%(lineno)d : %(message)s ')
    file_handler =lg.FileHandler("logsfile.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


