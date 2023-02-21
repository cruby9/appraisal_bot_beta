import sqlite3
import numpy as np
from scipy.optimize import least_squares
#working rpobust regression

conn = sqlite3.connect("./test_db.sqlite")
cursor = conn.cursor()

tables = ["all_sales", "comparable", "competing"]

def residuals(params, X, Y):
    a, b = params
    return Y - (a + b * X)

for table in tables:
    query = f"SELECT `Above Grade Finished Area`, `Close Price` FROM {table} WHERE `Above Grade Finished Area` IS NOT NULL AND `Close Price` IS NOT NULL"
    cursor.execute(query)

    X, Y = [], []
    for row in cursor.fetchall():
        X.append(row[0])
        Y.append(row[1])

    X = np.array(X)
    Y = np.array(Y)

    initial_guess = np.zeros(2)
    result = least_squares(residuals, initial_guess, args=(X, Y))

    a, b = result.x
    regression_equation = f"ŷ = {b}X + {a}"

    Y_pred = b * X + a
    MAE = np.mean(np.abs(Y - Y_pred))
    Std_Error_MAE = np.sqrt(np.sum((Y - Y_pred - MAE)**2) / (len(X) - 2))

    R_squared = 1 - np.sum((Y - Y_pred)**2) / np.sum((Y - np.mean(Y))**2)
    Std_Deviation = np.sqrt(np.sum((Y - Y_pred)**2) / len(X))

    print(f"Results for {table}:")
    print("Regression equation:", regression_equation)
    print("Mean Absolute Error (MAE):", round(MAE))
    print("Standard Error of MAE:", round(Std_Error_MAE))
    print("R-Squared:", round(R_squared, 2))
    print("Standard Deviation:", round(Std_Deviation))

conn.close()
