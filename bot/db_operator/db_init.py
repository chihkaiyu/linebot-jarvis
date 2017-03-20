import sys
from db_operator import db_operator

db = db_operator.DBConnector()
TABLE_NAME = 'USER'
TABLE_SCHEMA = {'userID': 'VARCHAR(64) NOT NULL',
                'favorite': 'VARCHAR(64)',
                'lastCmd': 'VARCHAR(64)',
                'PRIMARY KEY': '(userID)'}

if not db.is_table(TABLE_NAME):
    db.create(TABLE_NAME, TABLE_SCHEMA)
sys.exit(0)
