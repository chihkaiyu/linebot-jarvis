import sys
import db_operator

db = db_operator.DBConnector()
db.table_init('USER')
del db
sys.exit()
