import unittest
import pandas as pd
import sqlite3
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np

class TestRegression(unittest.TestCase):
    def test_regression_plots(self):
        def read_data_from_db(db_path, table_name):
            conn = sqlite3.connect(db_path)
            data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            return data

        db_path = "G:\\My Drive\\Github\\app_bot\\app_bot\\test_db.sqlite"
        table_names = ['all_sales', 'comparable', 'competing']

        for table_name in table_names:
            data = read_data_from_db(db_path, table_name)

            data = data[data["Close Price"] != 'None']

            try:
                X = data[["Above Grade Finished Area"]].dropna().astype(int)
                Y = data[["Close Price"]].dropna().astype(int)
            except ValueError:
                print(f"Skipping table '{table_name}': data is not integer type.")
                continue

            common_indices = X.index.intersection(Y.index)
            X = X.loc[common_indices].values.reshape(-1, 1)
            Y = Y.loc[common_indices].values.reshape(-1, 1)

            model = sm.OLS(Y, X).fit()

            X_prime = np.linspace(X.min(), X.max(), 100)[:, np.newaxis]
            Y_hat = model.predict(X_prime)

            plt.scatter(X, Y, alpha=0.5)
            plt.plot(X_prime, Y_hat, 'r', alpha=0.9)
            plt.xlabel("Above Grade Finished Area")
            plt.ylabel("Close Price")
            plt.title(f"Regression Plot for table '{table_name}'")
            plt.show()

