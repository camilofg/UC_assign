import psycopg2
import datetime
#from configparser import ConfigParser


class DbConn:
    def __init__(self, db_name, db_user, db_pass, db_host, db_port):
        self.conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
        self.conn.autocommit = True

    def overwrite_conn(self, db_name, db_user, db_pass, db_host, db_port):
        self.conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)

    def execute_query(self, query: object) -> object:
        try:
            cur = self.conn.cursor()
            cur.execute(query)
        except Exception as err:
            print(err)
        self.conn.commit()

    def execute_create_table(self, table_name, columns):
        data_type = " character varying(5000)"
        str_query = "CREATE TABLE "+table_name+"("
        column_names = ', '.join(list(map(lambda x: x + data_type, columns)))
        print(column_names)
        str_query += column_names + ")"
        default_value = datetime.datetime.today().strftime('%Y%m%d')
        query_ex = "ALTER TABLE " + table_name + " ADD COLUMN periodo varchar(20)" + " DEFAULT " + "'" + default_value + "';"

        try:
            cur = self.conn.cursor()
            cur.execute(str_query)
            cur.execute(query_ex)
        except Exception as err:
            print(err.pgcode)

    def execute_bulk(self, table_name, columns, file, delimiter=';', create_table=False):
        if create_table:
            self.execute_create_table(table_name, columns)

        query_bulk = "COPY "+table_name+"(" + ','.join(columns) + ") FROM " \
                                          "'" + file + "' DELIMITER '"+delimiter+"' CSV HEADER ENCODING 'LATIN1';"
        try:
            cur = self.conn.cursor()
            cur.execute(query_bulk)
        except Exception as err:
            print(err.pgcode)

    def execute_sp(self,  spName, periodo):
        try:
            cur = self.conn.cursor()
            cur.callproc(spName, ['20180514'])
            row = cur.fetchone()
            while row is not None:
                print(row)
                row = cur.fetchone()
            # close the communication with the PostgreSQL database server
            cur.close()

        except Exception as err:
            print(err.pgcode)
