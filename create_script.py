import pandas as pd
import os


class Create_Script:

    def __init__(self, file, schema):
        self.file = file
        self.schema = schema

    def call_tables(self):
        filename, file_extension = os.path.splitext(self.file)
        filename = filename.split('\\')[len(filename.split('\\'))-1]
        if file_extension == '.csv':
            return self.create_table(filename.replace(" ", "_"), pd.read_csv(self.file, encoding='latin1', error_bad_lines=False, delimiter=';'))

        else:
            xl = pd.ExcelFile(self.file, encoding='latin1', error_bad_lines=False)
            for itm in xl.sheet_names:
                print(itm)
                df1 = xl.parse(itm)
                return self.create_table(itm, df1)

    def create_table(self, tab_name, df1):
        tab_name = tab_name.replace(" ", "_")
        data_type = " character varying(5000)"
        str_query = " CREATE TABLE IF NOT EXISTS {}{}(".format(self.schema, tab_name)
        prefix = ""
        columns = ""
        for col in df1.axes[1]:
            if col == 'Unnamed: 0':
                str_query += prefix + '"ID" INTEGER'
                columns += prefix + '"ID"'
            elif col == 'Punto_Fisico_Inicial':
                str_query += prefix + '"INFR_I" ' + data_type
                columns += prefix + '"INFR_I" '
            elif col == 'Punto_Fisico_Final':
                str_query += prefix + '"INFR_F" ' + data_type
                columns += prefix + '"INFR_F" '
            else:
                str_query += prefix + '"' + col.replace(" ", "_") + '"' + data_type
                columns += prefix + '"' + col.replace(" ", "_") + '"'
            prefix = ", "
        str_query_org = ""
        if tab_name == "TRAMOS":
            str_query_org = str_query + ");"
            str_query += ', "CTO_COD" character varying(50), ' \
                         ' "ZONA" character varying(15), "NEW_SEMIAISLADO" character varying(1), ' \
                         ' "NEW_AISLAMIENTO" character varying(25), "NEW_NIVEL_TENSION" integer, ' \
                         ' "UC_015" character varying(15), "NEW_NEUTRO" character varying(1),' \
                         ' "UC_097" character varying(15), "NEW_CALIBRE" character varying(15), ' \
                         ' "NEW_TIPO_CABLE" character varying(50), "ID_CALIBRE" integer,' \
                         ' "NEW_CALIBRE_MM2" integer DEFAULT 0, "NEW_ID_CALIBRE" integer,' \
                         ' "NEW_INFR_F" character varying(150), "NEW_INFR_I" character varying(150)'
        str_query += ");"

        str_query += r" COPY {}{} ({}) FROM '{}' WITH DELIMITER '{}' CSV HEADER ENCODING 'LATIN1';".format(self.schema,
                                                                                                            tab_name,
                                                                                                            columns,
                                                                                                            self.file,
                                                                                                            ';')
        str_query += str_query_org.replace("TRAMOS", "TRAMOS_ORIGINAL")
        if tab_name == "TRAMOS":
            str_query += r" COPY {}{} FROM '{}' WITH DELIMITER '{}' CSV HEADER ENCODING 'LATIN1';".format(self.schema,
                tab_name+"_ORIGINAL", self.file, ';')
        print(str_query)
        return str_query
        #self.db.execute_query(str_query)
