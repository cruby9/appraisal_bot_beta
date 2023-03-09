import unittest
import pandas as pd
import sqlite3

def import_data(file_path, db_path, table_name):
    data = pd.read_csv(file_path)
    conn = sqlite3.connect(db_path)
    data.to_sql(table_name, conn, if_exists='replace', index=False)
    return data.shape[0]

def read_data_from_db(db_path, table_name):
    conn = sqlite3.connect(db_path)
    data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    return data

class TestImportData(unittest.TestCase):
    def test_formatting(self):
        file_paths = ["all_sales.csv", "comparable.csv", "competing.csv", "subject.csv"]
        db_path = "test_db.sqlite"
        table_names = ['all_sales', 'comparable', 'competing', 'subject']

        header_set = set()
        for file_path, table_name in zip(file_paths, table_names):
            data = pd.read_csv(file_path)
            header_set.add(tuple(data.columns))
            import_data(file_path, db_path, table_name)

        self.assertEqual(len(header_set), 1, "Headers are not the same in all files")

        header_from_db = set()
        for table_name in table_names:
            data_from_db = read_data_from_db(db_path, table_name)
            header_from_db.add(tuple(data_from_db.columns))

        self.assertEqual(header_from_db, header_set, "Headers in the database don't match the headers in the CSV files")

if __name__ == '__main__':
    unittest.main()










