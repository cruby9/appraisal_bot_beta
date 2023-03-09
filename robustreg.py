import sqlite3
import numpy as np
from sklearn.metrics import mean_absolute_error

conn = sqlite3.connect("./test_db.sqlite")
cursor = conn.cursor()

tables = ["all_sales", "comparable", "competing"]
output_dict = {}

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

    output_dict[table] = {
        "per_sq_ft_change": per_sq_ft_change,
        "MAE": mae,
        "SE_MAE": se_mae,
        "trim_setting": trim,
    }

print(output_dict)

