import dbOperator

db = dbOperator.DBConnector()
tableName = 'USER'
schema = {'userID': 'VARCHAR(64) NOT NULL', \
            'favorite': 'VARCHAR(64)', \
            'lastCmd': 'VARCHAR(64)', \
            'PRIMARY KEY': '(userID)'}

if not db.isTable(tableName):
    db.create(tableName, schema)
