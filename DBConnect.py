# -*- coding:UTF-8 -*-

import MySQLdb

class MYSQL():
    def __init__(self,database, config_file): #initialization
        server = config_file['Server'].strip()
        profile = config_file['Profile'].strip()
        pwd = config_file['Pwd'].strip()

        self.db = MySQLdb.connect(server, profile, pwd, database)
        self.db.set_character_set('utf8')
        self.cursor = self.db.cursor()

    def close(self):
        self.db.close

    def sql_select(self):
        pass
    
    def sql_insert(self, table_name, values):
        print('insert record to table ' + table_name + ' in process...')
        req = self.sql_retrevefields(table_name)
        value = ''
        for e in values:
            if value == '':
                if isinstance(e,int):
                    value = str(e)
                else:
                    value = "'" + e + "'"
            else:
                if isinstance(e,int):
                    value = value + "," + str(e)
                else:
                    value = value + ",'" + e + "'"

        fields = ','.join(f[0] for f in req)
        sql = 'insert into ' + table_name + ' (' + fields.strip()+ ') values (' + value + ')'
        self.cursor.execute(sql)
        self.db.commit()
        print('new record is inserted to ' + table_name)

    def sql_delete(self, table_name, values):
        pass

    def sql_update(self, table_name, values):
        pass
    
    def sql_retrevefields(self, table_name):
        sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '" + table_name + "';"
        self.cursor.execute(sql)
        fieldlist = []
        for row in self.cursor.fetchall():
            fieldlist.append(row)
        return fieldlist
