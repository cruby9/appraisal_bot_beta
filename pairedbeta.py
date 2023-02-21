import pandas as pd
from typing import List, Tuple
import csv
import os
import numpy as np
from itertools import combinations
import pandas as pd
import sqlite3
from collections import defaultdict
from typing import Dict
from typing import Dict, List, Tuple


tolerances = [50, 50, 50, 1000, 0, 0, 0]

matched_columns = ['Above Grade Finished Area', 'Below Grade Finished Area', 'Below Grade Unfinished Area',
                       'Lot Size Square Feet', 'Bathrooms Full', 'Bathrooms Half', 'Garage Spaces']
#we could remove on of these tolerances. 
tolerances = {
        'Above Grade Finished Area': 50,
        'Below Grade Finished Area': 50,
        'Below Grade Unfinished Area': 50,
        'Lot Size Square Feet': 1000,
        'Bathrooms Full': 0,
        'Bathrooms Half': 0,
        'Garage Spaces': 0
    }

import pandas as pd
import sqlite3

""" def import_data(db_path, table_name):
    #data = pd.read_csv(file_path)
    conn = sqlite3.connect(db_path)
    data.to_sql(table_name, conn, if_exists='replace', index=False)
    return data.shape[0] """

def read_data_from_db(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cols = ['"Above Grade Finished Area"', '"Below Grade Finished Area"', '"Below Grade Unfinished Area"', '"Lot Size Square Feet"', '"Bathrooms Full"', '"Bathrooms Half"', '"Garage Spaces"', '"Bathrooms Three Quarter"', '"Bathrooms One Quarter"', '"Close Price"', '"Listing Id"']
    data = pd.read_sql_query(f"SELECT {', '.join(cols)} FROM {table_name}", conn)

    print(data.head(1))
    print(data)
    return data

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    # remove any duplicates
    df = df.drop_duplicates()

    # replace empty cells with 0
    df = df.fillna(0)

    # split data into separate columns
    df = df[['Above Grade Finished Area', 'Below Grade Finished Area', 'Below Grade Unfinished Area', 
                    'Lot Size Square Feet', 'Bathrooms Full', 'Bathrooms Half',
                    'Bathrooms Three Quarter', 'Bathrooms One Quarter',
                    'Garage Spaces', 'Close Price', 
                    'Listing Id']]




    # rename columns
    df.columns = ['Above Grade Finished Area', 'Below Grade Finished Area', 'Below Grade Unfinished Area',
                  'Lot Size Square Feet', 'Bathrooms Full', 'Bathrooms Half', 'Bathrooms Three Quarter', 
                  'Bathrooms One Quarter', 'Garage Spaces', 'Close Price', 'Listing Id']




    # convert columns to appropriate data types
    df = df.astype({'Above Grade Finished Area': float, 'Below Grade Finished Area': float,
                    'Below Grade Unfinished Area': float, 'Lot Size Square Feet': float,
                    'Bathrooms Three Quarter': float, 'Bathrooms One Quarter':float,
                    'Bathrooms Full': int, 'Bathrooms Half': int, 'Garage Spaces': int,
                    'Close Price': float, 'Listing Id': str})
    print(df)
    return df

def process_bathrooms(df: pd.DataFrame) -> pd.DataFrame:
    # combine bathroom categories of original dataframe
    #Bathrooms Full with Bathrooms Three Quarter
    #Bathrooms Half with Bathrooms One Quarter
    df['Bathrooms Full'] = df['Bathrooms Full'] + df['Bathrooms Three Quarter']
    df['Bathrooms Half'] = df['Bathrooms Half'] + df['Bathrooms One Quarter']
    #drop the categories 'Bathrooms Three Quarter' and 'Bathrooms One Quarter' and make a new dataframe called df2
    df2 = df.drop(['Bathrooms Three Quarter', 'Bathrooms One Quarter'], axis=1)
    # add index row
    df2.reset_index(drop=True, inplace=True)
    #print new dataframe with combined bathroom categories and columns that were retained from the original dataframe
    print(df2)
    return df2 


    #create a function that takes the new dataframe and columns and compares them to each other
    #if the difference between the two columns is less than the tolerance, then it is a match
    #if the difference between the two columns is greater than the tolerance, then it is not a match
    #if the difference between the two columns is equal to the tolerance, then it is a match
    #then we are going to pair the two rows that have 6 matched out of 7 columns
    #there can be mulitple matches for each row
    #seperate the rows that have matches and the rows that do not have matches
    #if there are no matches, then we will return an empty dataframe that says 'no matches found try again'
    #if there are matches, then we will return a dataframe that shows the two listings that are paired together and the column that they matched on seperated by the column header and grouped togehter by the two listings
    #if there are multiple matches, then we will return a dataframe that shows the two listings that are paired together and the column that they matched on seperated column headers and grouped together
    #there can be several matches for each row and several matches for each column
    #seperate each column difference pairing into seperate csv files and name them by the two or more listings that they are paired together
    #seperate each pairing by Listing Id 1 and Listing Id 2 and Close Price 1 and Close Price 2 and then the column that they matched on value 1 and value 2


def match_pairs(df: pd.DataFrame, column_names: List[str], num_rows: int) -> Dict[str, List[Tuple[str, str, float, float, float, float]]]:
    paired_properties = defaultdict(list)
    for i in range(num_rows):
        row1 = df.iloc[i]
        for j in range(i + 1, num_rows):
            row2 = df.iloc[j]
            if row1['Close Price'] == 0 or row2['Close Price'] == 0:
                continue
            num_diffs = sum(abs(row1[col] - row2[col]) > tolerances[col] for col in tolerances)
            if num_diffs == 1:
                non_matching_col = next(col for col in column_names if abs(row1[col] - row2[col]) > tolerances[col])
                paired_properties[non_matching_col].append(
                    (row1['Listing Id'], row2['Listing Id'], row1['Close Price'], row2['Close Price'], row1[non_matching_col], row2[non_matching_col]))
    print(paired_properties)
    return paired_properties

def write_to_csv(grouped_matches, columns, output_folder='testdata'):
    os.makedirs(output_folder, exist_ok=True)
    for col in columns:
        if col not in grouped_matches:
            continue
        file_name = f"{col}_matches.csv"
        with open(f"{output_folder}/{file_name}", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Listing Id 1', 'Listing Id 2', 'Close Price 1', 'Close Price 2', f'{col} 1', f'{col} 2', 'Close Price Difference', f'{col} Difference', 'Price to Value Ratio'])
            for pair in grouped_matches[col]:
                close_price_diff = abs(pair[2] - pair[3])
                col_diff = abs(pair[4] - pair[5])
                if col_diff != 0:
                    ratio = close_price_diff / col_diff
                else:
                    ratio = 0
                row = pair[0:2] + (pair[2], pair[3], pair[4], pair[5], close_price_diff, col_diff, ratio)
                writer.writerow(row)



def main():
    # read in data from SQLite database
    db_path = 'test_db.sqlite'
    table_name = 'all_sales'
    df = read_data_from_db(db_path, table_name)

    # preprocess data
    df = process_data(df)
    df = process_bathrooms(df)

    # match pairs of properties
    num_rows = len(df)
    grouped_matches = match_pairs(df, matched_columns, num_rows)

    # write results to CSV files
    write_to_csv(grouped_matches, matched_columns)

if __name__ == '__main__':
    main()



