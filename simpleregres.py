import sqlite3
import numpy as np
#working simple regression
conn = sqlite3.connect("./test_db.sqlite")
cursor = conn.cursor()

tables = ["all_sales", "comparable", "competing"]

for table in tables:
    query = f"SELECT `Above Grade Finished Area`, `Close Price` FROM {table} WHERE `Above Grade Finished Area` IS NOT NULL AND `Close Price` IS NOT NULL"
    cursor.execute(query)

    X, Y = [], []
    for row in cursor.fetchall():
        X.append(row[0])
        Y.append(row[1])

    X = np.array(X)
    Y = np.array(Y)

    mean_X = np.mean(X)
    mean_Y = np.mean(Y)

    SSX = np.sum((X - mean_X)**2)
    SP = np.sum((X - mean_X) * (Y - mean_Y))

    b = SP / SSX
    a = mean_Y - b * mean_X

    b = round(b)
    a = round(a)

    regression_equation = f"ŷ = {b}X + {a}"

    Y_pred = b * X + a
    MAE = np.mean(np.abs(Y - Y_pred))
    Std_Error_MAE = np.sqrt(np.sum((Y - Y_pred - MAE)**2) / (len(X) - 2))

    R_squared = 1 - np.sum((Y - Y_pred)**2) / np.sum((Y - mean_Y)**2)
    Std_Deviation = np.sqrt(np.sum((Y - Y_pred)**2) / len(X))

    print(f"Results for {table}:")
    print("Regression equation:", regression_equation)
    print("Mean Absolute Error (MAE):", round(MAE))
    print("Standard Error of MAE:", round(Std_Error_MAE))
    print("R-Squared:", round(R_squared, 2))
    print("Standard Deviation:", round(Std_Deviation))

conn.close()














