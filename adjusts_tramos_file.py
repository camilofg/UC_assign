from sqlalchemy import create_engine
import pandas as pd
import query_strings as qs
import postgres_conn as pg_conn
import datetime
import os
from bs4 import BeautifulSoup as Soup
import pyodbc as odbc
import pandas as pd
import create_script as cs


class AdjustsTramosFile:

    def __init__(self, xml_config):
        with open(xml_config, 'r', encoding='utf-8-sig') as my_file:
            soup = Soup(my_file)
            self.db_name = soup.find("db-name").next
            self.db_base_name = soup.find("db-base-name").next
            self.db_user = soup.find("db-user").next
            self.db_pass = soup.find("db-pass").next
            self.db_host = soup.find("db-host").next
            self.db_port = soup.find("db-port").next
            self.db = pg_conn.DbConn(self.db_base_name,
                                     self.db_user,
                                     self.db_pass,
                                     self.db_host,
                                     self.db_port
                                     )
            self.resources = soup.find("resource-path").next
            self.sources = soup.find("sources-path").next
            self.db_route = soup.find("db_route").next
            self.db_schema = None if soup.find("db_schema") is None else soup.find("db_schema").next + '.'
            self.db_created = False

    def load_access_tables(self):
        for itm in os.listdir(self.db_route):
            if itm.endswith('.mdb') or itm.endswith('.accdb'):
                conn = odbc.connect(
                    r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + self.db_route + itm + ';')
                if not self.db_created:
                    self.create_clean_database()
                    if self.db_schema is not None:
                        self.create_schema()
                cursor = conn.cursor()
                table_names = [x[2] for x in cursor.tables().fetchall() if x[3] == 'TABLE']
                filename, file_extension = os.path.splitext(self.db_route)
                file_route = filename.split('\\')
                del file_route[-1]
                for item in table_names:
                    sql_query = 'select * from ' + item
                    data = pd.read_sql(sql_query, conn)
                    route_f = "\\".join(file_route) + "\\" + item.upper().replace("TBL_", "") + '.csv'
                    data.to_csv(route_f, sep=";")
                    creator = cs.Create_Script(route_f, self.db_schema)
                    query_str = creator.call_tables()
                    self.db.execute_query(query_str)

    def create_clean_database(self):
        str_create_db = 'CREATE DATABASE ' + self.db_name
        self.db.execute_query(str_create_db)
        self.db.overwrite_conn(self.db_name,
                               self.db_user,
                               self.db_pass,
                               self.db_host,
                               self.db_port)
        self.db_created = True

    def create_schema(self):
        str_create_schema = 'CREATE SCHEMA ' + self.db_schema[:-1]
        self.db.execute_query(str_create_schema)

    def execute_scripts(self):
        list_files = os.listdir(self.resources)
        for x in list_files:
            print(x)
            try:
                with open(os.path.abspath(self.resources + x), 'r', encoding='utf-8-sig') as myfile:
                    if x == '98.CREATE FINAL FILE.txt':
                        print('test')
                    query_str = myfile.read().format(SCHEMA=self.db_schema, ROUTE=self.sources)
                self.db.execute_query(query_str)
            except Exception as err:
                print(err)
