from sqlalchemy import create_engine
import pandas as pd
import query_strings as qs
import postgres_conn as pg_conn
import datetime
import os
from bs4 import BeautifulSoup as Soup


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

    def start_clean_file(self):
        str_create_db = 'CREATE DATABASE ' + self.db_name
        self.db.execute_query(str_create_db)
        self.db.overwrite_conn(self.db_name,
                               self.db_user,
                               self.db_pass,
                               self.db_host,
                               self.db_port)
        list_files = os.listdir(self.resources)
        for x in list_files:
            print(x)
            with open(os.path.abspath(self.resources + x), 'r', encoding='utf-8-sig') as myfile:
                query_str = myfile.read().format(self.sources)
            self.db.execute_query(query_str)

