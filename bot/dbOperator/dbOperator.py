import mysql.connector

class DBConnector(object):
    def __init__(self):
        self.connection = (mysql.connector.connect(
                            user='bot', password='yurabuai99',
                            database='linebot', host='db'))
        
        self.cursor = self.connection.cursor()
        self.insQry = ('INSERT INTO {TABLE}\n'
                        '({COLUMN})\n'
                        'VALUES ({VALUE})')

        self.updateQry = ('UPDATE {TABLE}\n'
                            'SET {COLUMN}\n'
                            'WHERE {CONDITION}')
        self.createTbl = ('CREATE TABLE {TABLE} (\n'
                            '{SCHEMA})')
        self.query = ('SELECT {COLUMN}\n'
                            'FROM {TABLE}\n'
                            'WHERE {CONDITION}')
        
        self.addSingleQuo = lambda val: '\'{VAL}\''.format(VAL=val) if type(val) is str else str(val)

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def isRecord(self, tableName, column, target):
        mysqlQuery = ('SELECT EXISTS(SELECT * FROM {TABLE} WHERE {COLUMN}={TARGET})'
                .format(TABLE=tableName, 
                        COLUMN=column, 
                        TARGET=self.addSingleQuo(target)))
        self.cursor.execute(mysqlQuery)
        res = self.cursor.fetchall()
        return res[0][0]
    
    def isTable(self, tableName):
        self.cursor.execute('SHOW TABLES LIKE \'{TABLE}\''.format(TABLE=tableName))
        res = self.cursor.fetchall()
        doesExist = lambda res: True if res else False
        return doesExist(res)
    
    def query(self, tablename, column, condition):
        mysqlQuery = self.queryData.format(COLUMN=column \
                                            TALBE=talbeName \
                                            CONDITION=condition)
        self.cursor.execute(mysqlQuery)
        return self.cursor.fetchall()[0][0]

    def insert(self, tableName, data):
        mysqlQuery = self.insQry.format(TABLE=tableName, \
                                        COLUMN=', '.join([col for col in data.keys()]), \
                                        VALUE=', '.join([self.addSingleQuo(data[key]) for key in data.keys()]))
        try:
            self.cursor.execute(mysqlQuery)
            self.connection.commit()
        except:
            self.connection.rollback()

    def create(self, tableName, schema):
        mysqlQuery = self.createTbl.format(TABLE=tableName, \
                                            SCHEMA=', \n'.join(['{NAME} {TYPE}' \
                                                                .format(NAME=key, TYPE=schema[key]) for key in schema.keys()]))
        try:
            self.cursor.execute(mysqlQuery)
            self.connection.commit()
        except:
            self.connection.rollback()

    def update(self, tableName, data, condition):
        mysqlQuery = self.updateQry.format(TABLE=tableName, \
                                            COLUMN=', '.join(['{}={}'.format(key, self.addSingleQuo(data[key])) \
                                                                for key in data.keys()]),\
                                            CONDITION=condition)
        try:
            self.cursor.execute(mysqlQuery)
            self.connection.commit()
        except:
            self.connection.rollback()
    
    def displayRec(self, tableName):
        self.cursor.execute('SELECT * FROM {TABLE}'.format(TABLE=tableName))
        print(self.cursor.fetchall())


