import mysql.connector

class DBConnector(object):
    def __init__(self):
        self.db = (mysql.connector.connect(
                                user='kai', password='yurabuai99',
                                database='linebot', host='127.0.0.1'))
        self.cursor = self.db.cursor()
        self.insert = """INSERT INTO USER
                        (userID, favorite, lastCmd)
                        VALUES (%s, %s, %s)"""
        
        self.update = """UPDATE USER
                         SET lastCmd=%(lastCmd)s
                         WHERE userID=%(userID)s"""

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def isUser(self, userID):
        pass

    def addUser(self, userID):
        try:
            self.cursor.execute(self.insert, userID)
            self.db.commit()
        except:
            self.db.rollback()


    def setFavorite(self, userID, favorite):
        pass
    def updateLastCmd(self, userID, lastCmd):
        try:
            self.cursor.execute(self.update, {'userID': userID, 'lastCmd': lastCmd})
        except:
            self.db.rollback()

    def isTable(self, tableName):
        pass
