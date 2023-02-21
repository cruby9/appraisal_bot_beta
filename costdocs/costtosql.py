import pandas as pd
import sqlite3

def import_data(file_path, db_path, table_name):
    data = pd.read_excel(file_path, engine='openpyxl')
    data = data.fillna(0)
    conn = sqlite3.connect(db_path)
    data.to_sql(table_name, conn, if_exists='replace', index=False)
    return data.shape[0]


import_data('./costdocs/cost_tables.xlsx', 'cost_data.db', 'cost_data')












