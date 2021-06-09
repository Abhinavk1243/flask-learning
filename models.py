import mysql.connector as msc
import logging as lg 
import configparser

def getconfig(section,key):
    """Method use to read the value of key in congfig file i.e .cfg extension file

    Args:
        section (string): section name in cfg file whose value want to read
        key (string): key identification of section whose value want to read

    Returns:
        string: value of corresonding section key
    """
    parser = configparser.ConfigParser()
    parser.read('credential.cfg')
    return parser.get(section,key)  

def read_configconnection():
    """Metod is use to connect database with python 

    Returns:
        connection : myslconnection
    """
    mydb=msc.connect(host=getconfig("mysql","host"),
                    user=getconfig("mysql","user"),
                    database=getconfig("mysql","database"),
                    password=getconfig("mysql","password"))
    return mydb

def logger():
    logger = lg.getLogger(__name__)
    logger.setLevel(lg.DEBUG)
    formatter = lg.Formatter('%(asctime)s : %(name)s : %(filename)s : %(levelname)s\
                             :%(funcName)s :%(lineno)d : %(message)s ')
    file_handler =lg.FileHandler("D:/ashu\GitHub/python-learning/scripts/loggers_files/logsfile.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
