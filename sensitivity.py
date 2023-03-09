import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import hashlib

conn = sqlite3.connect("./test_db.sqlite")
cursor = conn.cursor()

tables = ["all_sales", "comparable", "competing"]

for table in tables:
    query = f"SELECT `Above Grade Finished Area`, `Close Price` FROM {table} WHERE `Above Grade Finished Area` IS NOT NULL AND `Close Price` IS NOT NULL"
    cursor.execute(query)
    data = cursor.fetchall()
    data = np.array(data)

    x = data[:, 0]
    y = data[:, 1]

    lower_bound_x = np.percentile(x, 2.5)
    upper_bound_x = np.percentile(x, 97.5)
    lower_bound_y = np.percentile(y, 2.5)
    upper_bound_y = np.percentile(y, 97.5)

    trimmed_data = [(xi, yi) for xi, yi in zip(x, y) if lower_bound_x <= xi <= upper_bound_x and lower_bound_y <= yi <= upper_bound_y]
    trimmed_data = np.array(trimmed_data)

    x = trimmed_data[:, 0]
    y = trimmed_data[:, 1]

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)

    per_sq_ft_change = int(z[0])

    y_pred = p(x)
    mae = int(mean_absolute_error(y, y_pred))
    se_mae = int(np.std(y - y_pred) / np.sqrt(len(y)))
    trim = int(mae * 5 / 100)

    plt.scatter(x, y)
    plt.plot(x, p(x), "r")
    plt.xlabel("Above Grade Finished Area (Square Feet)")
    plt.ylabel("Close Price (USD)")
    plt.title(f"Sensitivity Analysis of Close Price on Above Grade Finished Area ({table})")
    plt.show()

    # create hash object and update with table name, per sq ft change, mae, se_mae, and trim
    h = hashlib.sha256()
    h.update(table.encode())
    h.update(str(per_sq_ft_change).encode())
    h.update(str(mae).encode())
    h.update(str(se_mae).encode())
    h.update(str(trim).encode())
    hash_output = h.hexdigest()

    print(f"Table: {table}")
    print(f"Result: Per Square Foot Change: {per_sq_ft_change} USD")
    print(f"Mean Absolute Error (MAE): {mae} USD")
    print(f"Standard Error of MAE: {se_mae} USD")
    print(f"Trim Setting 5%: {trim} USD")
    print(f"Hash Output: {hash_output}")
    print()





