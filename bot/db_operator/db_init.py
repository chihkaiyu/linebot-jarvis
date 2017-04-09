import sys
from db_operator import DatabaseConnector

db = DatabaseConnector()
db.table_init('USER')
del db
sys.exit()
