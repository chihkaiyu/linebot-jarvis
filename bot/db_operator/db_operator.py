# -*- coding: utf-8 -*-
"""This is a module to deal with MySQL database"""

import json
import os
import mysql.connector


class DatabaseConnector(object):
    """A MySQL database connector"""

    def __init__(self, mysql_login_info=None):
        if not isinstance(mysql_login_info, dict):
            folder_name = os.path.abspath(os.pardir)
            config_path = os.path.join(folder_name, 'credential',
                                       'mysql_config.json')
            mysql_login_info = json.load(open(config_path))
        self.connection = (mysql.connector.connect(**mysql_login_info))

        self.cursor = self.connection.cursor()
        self.mysql_insert = ('INSERT INTO {TABLE}\n'
                             '({COLUMN})\n'
                             'VALUES ({VALUE})')

        self.mysql_update = ('UPDATE {TABLE}\n'
                             'SET {COLUMN}\n'
                             'WHERE {CONDITION}')

        self.mysql_create = ('CREATE TABLE {TABLE} (\n'
                             '{SCHEMA})')

        self.mysql_select = ('SELECT {COLUMN}\n'
                             'FROM {TABLE}\n'
                             'WHERE {CONDITION}')

        self.add_single_quo = (lambda val: '\'{VAL}\''.format(VAL=val)
                               if isinstance(val, str) else str(val))

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def is_record(self, table_name, column, target):
        """Return whether a record exists in table"""

        mysql_query = ('SELECT EXISTS ( \n'
                       'SELECT * FROM {TABLE} \n'
                       'WHERE {COLUMN}={TARGET})'
                       .format(TABLE=table_name,
                               COLUMN=column,
                               TARGET=self.add_single_quo(target)))
        self.cursor.execute(mysql_query)
        res = self.cursor.fetchall()
        return res[0][0]

    def is_table(self, table_name):
        """Return wheter a table exists"""

        self.cursor.execute('SHOW TABLES LIKE \'{TABLE}\''
                            .format(TABLE=table_name))
        res = self.cursor.fetchall()
        # does_exist = lambda res: True if res else False
        return res

    def query(self, table_name, column, condition):
        """Query database"""

        mysql_query = self.mysql_select.format(COLUMN=column,
                                               TABLE=table_name,
                                               CONDITION=condition)
        self.cursor.execute(mysql_query)
        return self.cursor.fetchall()[0][0]

    def insert(self, table_name, data):
        """Insert a record to database"""

        mysql_query = (self.mysql_insert
                       .format(TABLE=table_name,
                               COLUMN=', '.join([col for col in data.keys()]),
                               VALUE=', '.join([self.add_single_quo(data[key])
                                                for key in data.keys()])))
        try:
            self.cursor.execute(mysql_query)
            self.connection.commit()
        except:
            self.connection.rollback()

    def create(self, table_name, schema):
        """Create a table in database"""

        schema_format = ['{NAME} {TYPE}'.format(NAME=key, TYPE=schema[key])
                         for key in schema.keys()]
        mysql_query = (self.mysql_create
                       .format(TABLE=table_name,
                               SCHEMA=', \n'.join(schema_format)))
        try:
            self.cursor.execute(mysql_query)
            self.connection.commit()
        except:
            self.connection.rollback()

    def update(self, table_name, data, condition):
        """Update a record in database"""

        data_format = ['{KEY}={VALUE}'
                       .format(KEY=key, VALUE=self.add_single_quo(data[key]))
                       for key in data.keys()]
        mysql_query = (self.mysql_update
                       .format(TABLE=table_name,
                               COLUMN=', '.join(data_format),
                               CONDITION=condition))
        try:
            self.cursor.execute(mysql_query)
            self.connection.commit()
        except:
            self.connection.rollback()

    def table_init(self, table_name):
        """Initialize a table if not exists"""

        table_schema = {'userID': 'VARCHAR(64) NOT NULL',
                        'favorite': 'VARCHAR(64)',
                        'lastCmd': 'VARCHAR(64)',
                        'PRIMARY KEY': '(userID)'}
        if not self.is_table(table_name):
            self.create(table_name, table_schema)

    def display_rec(self, table_name):
        """Display a record in database"""

        self.cursor.execute('SELECT * FROM {TABLE}'.format(TABLE=table_name))
        print(self.cursor.fetchall())
