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
        
        self.addSingleQuo = lambda val: ('\'{VAL}\''.format(VAL=val) if type(val) is str
                                                                        else str(val))

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def isRecord(self, tableName, column, target):
        query = ('SELECT EXISTS(SELECT * FROM {TABLENAME} WHERE {COLUMN}={TARGET})'
                .format(TABLENAME=tableName, 
                        COLUMN=column, 
                        TARGET=self.addSingleQuo(target)))
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res[0][0]


    def insert(self, tableName, data):
        query = self.insQry.format(TABLE=tableName,
                                    COLUMN=', '.join([col for col in data.keys()]),
                                    VALUE=', '.join([self.addSingleQuo(data[key]) for key in data.keys()]))
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            self.connection.rollback()

    def create(self, tableName, schema):
        query = self.createTbl.format(TABLE=tableName, 
                                        SCHEMA=', \n'.join(['{NAME} {TYPE}' \
                                                .format(NAME=key, TYPE=schema[key]) for key in schema.keys()]))
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            self.connection.rollback()

    def update(self, tableName, data, condition):
        query = self.updateQry.format(TABLE=tableName,
                                        COLUMN=', '.join(['{}={}'.format(key, self.addSingleQuo(data[key]))
                                                            for key in data.keys()]),
                                        CONDITION=condition)
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            self.connection.rollback()
    
    def displayRec(self, tableName):
        self.cursor.execute('SELECT * FROM {TABLENAME}'.format(TABLENAME=tableName))
        print(self.cursor.fetchall())

    def isTable(self, tableName):
        self.cursor.execute('SHOW TABLES LIKE \'{TABLENAME}\''.format(TABLENAME=tableName))
        res = self.cursor.fetchall()
        doesExist = lambda res: True if res else False
        return doesExist(res)
