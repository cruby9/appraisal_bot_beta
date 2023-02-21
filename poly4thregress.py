import sqlite3
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

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

    print(f"Results for {table}:")
    print("Regression equation:", model.intercept_, model.coef_)
    equation = np.poly1d(np.flip(np.append(model.intercept_, model.coef_)))
    print("Polynomial equation:", equation)
    print("Mean Absolute Error (MAE):", round(MAE))
    print("Standard Error of MAE:", round(Std_Error_MAE))
    print("R-Squared:", round(R_squared, 2))
    print("Standard Deviation:", round(Std_Deviation))

conn.close()

