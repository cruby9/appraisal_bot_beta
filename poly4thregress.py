import sqlite3
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import hashlib

conn = sqlite3.connect("./test_db.sqlite")
cursor = conn.cursor()

tables = ["all_sales", "comparable", "competing"]

for table in tables:
    print(f"Processing table '{table}'...")
    query = f"SELECT `Above Grade Finished Area`, `Close Price` FROM {table} WHERE `Above Grade Finished Area` IS NOT NULL AND `Close Price` IS NOT NULL"
    cursor.execute(query)

    X, Y = [], []
    for row in cursor.fetchall():
        X.append(row[0])
        Y.append(row[1])

    X = np.array(X).reshape(-1, 1)
    Y = np.array(Y)

    poly_reg = PolynomialFeatures(degree=4)
    X_poly = poly_reg.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, Y)

    Y_pred = model.predict(X_poly)

    MAE = np.mean(np.abs(Y - Y_pred))
    Std_Error_MAE = np.sqrt(np.sum((Y - Y_pred - MAE)**2) / (len(X) - 2))

    R_squared = model.score(X_poly, Y)
    Std_Deviation = np.sqrt(np.sum((Y - Y_pred)**2) / len(X))

    for i, row in enumerate(cursor.fetchall()):
        print(f"Processing row {i+1}...")
        row_hash = hashlib.sha256(str(row).encode()).hexdigest()
        key = f"{table}_{i+1}"
        values = {
            "Above Grade Finished Area": row[0],
            "Close Price": row[1],
            "Predicted Close Price": Y_pred[i],
            "Absolute Error": np.abs(Y[i] - Y_pred[i]),
            "Mean Absolute Error": MAE,
            "Standard Error of MAE": Std_Error_MAE,
            "R-Squared": R_squared,
            "Standard Deviation": Std_Deviation,
            
        }
        print(f"{key}: {row_hash} {values}")
        

    print(f"Finished processing table '{table}'.")
    print(MAE, Std_Error_MAE, R_squared, Std_Deviation) 
    print()

conn.close()



