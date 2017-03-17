from db_operator import db_operator

db = db_operator.DBConnector()
table_name = 'USER'
schema = {'userID': 'VARCHAR(64) NOT NULL',
          'favorite': 'VARCHAR(64)',
          'lastCmd': 'VARCHAR(64)',
          'PRIMARY KEY': '(userID)'}

if not db.is_table(table_name):
    db.create(table_name, schema)
