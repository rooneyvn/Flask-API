# -*- coding: utf-8 -*-
__author__ = 'NguyenPV'
import pymysql
from collections import OrderedDict


class MysqlPython(object):
    """
        Python Class for connecting  with MySQL server and accelerate development project using pymysql
        Extremely easy to learn and use, friendly construction.
    """

    __instance = None   # Keep instance reference 
    __host = None
    __post = None
    __user = None
    __password = None
    __database = None
    __session = None
    __connection = None

       
    ''' disable for multi connection
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            #cls.__instance = super(MysqlPython, cls).__new__(cls,*args,**kwargs)   #python 2
            cls.__instance = super(MysqlPython, cls).__new__(cls)  #python 3
        return cls.__instance
    #end __new__
    '''
    def __init__(self, host='localhost', port=3306, user='root', password='', database=''):
        self.__host = host
        self.__post = port
        self.__user = user
        self.__password = password
        self.__database = database
    # End def __init__
    
    def __open(self):
        try:
            self.__connection = pymysql.connect(host=self.__host, port=self.__post,user=self.__user, password=self.__password, db=self.__database, cursorclass=pymysql.cursors.DictCursor, charset="utf8")
            self.__session = self.__connection.cursor()            
        except Exception as e:
            print(e)   
    #end __open       
    
    def execute(self, sql):
        self.__open()
        rs = self.__session.execute(sql)        
        self.__close()
        return rs
    # End execute                 
    
    def query(self, sql):
        self.__open()
        self.__session.execute(sql)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]
        self.__close()

        return result
    # End query
        
    def count(self, sql):
        self.__open()
        self.__session.execute(sql)
        result = self.__session.fetchone()
        self.__close()

        return result
    # End query
    
    def select(self, table, where=None, *args, **kwargs):
        result = None
        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for i, key in enumerate(keys):
            query += "`"+key+"`"
            if i < l:
                query += ","
        # End for keys

        query += 'FROM %s' % table
        #query += 'FROM `%s`' % table

        if where:
            query += " WHERE %s" % where
        # End if where

        self.__open()
        self.__session.execute(query, values)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]
        self.__close()

        return result
    # End def select

    def update(self, table, where=None, *args, **kwargs):
        query = "UPDATE %s SET " % table
        keys = kwargs.keys()
        values = tuple(kwargs.values()) + tuple(args)
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`"+key+"` = %s"
            if i < l:
                query += ","
            # End if i less than 1
        # End for keys
        query += " WHERE %s" % where

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        update_rows = self.__session.rowcount
        self.__close()

        return update_rows
    # End function update

    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %s " % table
        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + \
                ") VALUES (" + ",".join(["%s"]*len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"]*len(values)) + ")"

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()
        self.__close()
        return self.__session.lastrowid
    # End def insert

    def delete(self, table, where=None, *args):
        query = "DELETE FROM %s" % table
        if where:
            query += ' WHERE %s' % where

        values = tuple(args)

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        delete_rows = self.__session.rowcount
        self.__close()

        return delete_rows
    # End def delete

    def select_advanced(self, sql, *args):
        od = OrderedDict(args)
        query = sql
        values = tuple(od.values())
        self.__open()
        self.__session.execute(query, values)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]

        self.__close()
        return result
    # End def select_advanced    
    def execute_with_pandas(self, sql):
        import pandas        
        self.__open()
        results = pandas.read_sql_query(sql, self.__connection)           
        self.__close()
        return results
        
    #  close database connection 
    def __close(self):
        self.__connection.close()
    #end __close        
     
# End class
