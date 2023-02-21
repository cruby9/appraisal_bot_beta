import unittest
import csv
import os
import pandas as pd
from pairsalealpha import get_tolerance
from pairsalealpha import process_data
from pairsalealpha import match_properties
from pairsalealpha import tolerances
from pairedsalealpha2 import compare_rows
from pairedsalealpha2 import csv_to_pandas
from pairedsalealpha2 import match_pairs
from pairedsalealpha2 import combine_bathrooms


""" def oldget_tolerance(column_name):
    tolerances = {
        'Above Grade Finished Area': 50.0,
        'Below Grade Finished Area': 50.0,
        'Below Grade Unfinished Area': 50.0,
        'Lot Size Square Feet': 1000.0,
        'Bathrooms Full': 0.0,
        'Bathrooms Half': 0.0,
        'Garage Spaces': 0.0
    }
    return tolerances.get(column_name, 0)
 """
""" def match_properties(database, column_name):
    paired_properties = []
    for i in range(len(database)):
        for j in range(i + 1, len(database)):
            difference_count = 0
            for column in column_name:
                value1 = database[i].get(column, '')
                value2 = database[j].get(column, '')
                if value1 == '' or value2 == '':
                    continue
                else:
                    value1 = float(value1)
                    value2 = float(value2)

                tolerance = get_tolerance(column)
                if abs(value1 - value2) > tolerance:
                    difference_count += 1

            if difference_count <= 6:
                paired_properties.append((database[i], database[j]))
    return paired_properties """

class appBot(unittest.TestCase):
    def test_csv_to_pandas(self):
            file_path = "./testdata/sample.csv"
            columns = ['Listing Id', 'Close Price', 'Above Grade Finished Area', 'Below Grade Finished Area', 'Below Grade Unfinished Area', 'Lot Size Square Feet', 'Bathrooms Full', 'Bathrooms Half', 'Garage Spaces']

            df = csv_to_pandas(file_path, columns)

            # Check if the DataFrame has the correct number of rows and columns
            self.assertEqual(df.shape[0], 100)
            self.assertEqual(df.shape[1], 9)

            # Check if the DataFrame contains only the specified columns
            self.assertEqual(set(df.columns), set(columns))

            # Check if the missing values have been filled with 0
            self.assertEqual(df.isnull().sum().sum(), 0)
    
    def test_combine_bathrooms(self):
        # Create a sample DataFrame with columns 'Bathrooms Full', 'Bathrooms Half', 'Bathrooms One Quarter', 'Bathrooms Three Quarter'
        sample_df = pd.DataFrame({'Bathrooms Full': [1, 2, 3, 4],
                                'Bathrooms Half': [1, 1, 1, 1],
                                'Bathrooms One Quarter': [1, 1, 1, 1],
                                'Bathrooms Three Quarter': [1, 1, 1, 1]})

        # Combine the columns using the combine_bathrooms function
        combined_df = combine_bathrooms(sample_df)

        # Check if the 'Bathrooms Three Quarter' column has been added to the 'Bathrooms Full' column
        self.assertEqual(combined_df['Bathrooms Full'].tolist(), [2, 2, 4, 5])

        # Check if the 'Bathrooms Three Quarter' column has been dropped
        self.assertNotIn('Bathrooms Three Quarter', combined_df.columns)

        # Check if the 'Bathrooms One Quarter' column has been added to the 'Bathrooms Half' column
        self.assertEqual(combined_df['Bathrooms Half'].tolist(), [2, 2, 2, 2])

        # Check if the 'Bathrooms One Quarter' column has been dropped
        self.assertNotIn('Bathrooms One Quarter', combined_df.columns)
    def test_match_properties():
    # Create a test DataFrame with two rows
    test_data = {'Above Grade Finished Area': [1000, 1100],
                 'Below Grade Finished Area': [500, 550],
                 'Below Grade Unfinished Area': [0, 0],
                 'Lot Size Square Feet': [5000, 5500],
                 'Bathrooms Full': [2, 2],
                 'Bathrooms Half': [1, 1],
                 'Garage Spaces': [2, 2],
                 'Close Price': [200000, 220000],
                 'Listing Id': [1, 2]}
    test_df = pd.DataFrame(data=test_data)

    # Set the tolerances and AGFA column name
    tolerances = [50, 50, 50, 1000, 0, 0, 0]
    agfa_col_name = 'Above Grade Finished Area'

    # Call the match_properties function and check that it returns an empty list
    paired_properties = match_properties(test_df, tolerances, agfa_col_name)
    assert paired_properties == []

    # Change the first row to be similar enough to the second row to make a pair
    test_df.iloc[0, 0] = 1100
    paired_properties = match_properties(test_df, tolerances, agfa_col_name)
    assert paired_properties == [(test_df.iloc[0], test_df.iloc[1])]




    def test_get_tolerance(self):
        test_data = [
            {'Listing Id': 1, 'Close Price': 180000, 'Above Grade Finished Area': 1500, 'Below Grade Finished Area': 500, 'Below Grade Unfinished Area': 100, 'Lot Size Square Feet': 5000, 'Bathrooms Full': 2, 'Bathrooms Half': 1, 'Garage Spaces': 2},
            {'Listing Id': 2, 'Close Price': 170000, 'Above Grade Finished Area': 1700, 'Below Grade Finished Area': 550, 'Below Grade Unfinished Area': 150, 'Lot Size Square Feet': 5500, 'Bathrooms Full': 2, 'Bathrooms Half': 1, 'Garage Spaces': 2}
        ]
        matched_columns = ['Above Grade Finished Area', 'Below Grade Finished Area', 'Below Grade Unfinished Area', 'Lot Size Square Feet', 'Bathrooms Full', 'Bathrooms Half', 'Garage Spaces']

        df = pd.DataFrame(test_data)
        result = compare_rows(df, matched_columns)

        expected_output = [(0, 1, 'Above Grade Finished Area')]
        print("Result:", result)
        print("Expected output:", expected_output)

        self.assertEqual(result, expected_output)

        import pandas as pd


def test_match_pairs():
    data = [
        {'Listing Id': 1, 'Close Price': 180000, 'Above Grade Finished Area': 1500, 'Below Grade Finished Area': 500, 'Below Grade Unfinished Area': 100, 'Lot Size Square Feet': 5000, 'Bathrooms Full': 2, 'Bathrooms Half': 1, 'Garage Spaces': 2},
        {'Listing Id': 2, 'Close Price': 170000, 'Above Grade Finished Area': 1700, 'Below Grade Finished Area': 550, 'Below Grade Unfinished Area': 150, 'Lot Size Square Feet': 5500, 'Bathrooms Full': 2, 'Bathrooms Half': 1, 'Garage Spaces': 2},
        {'Listing Id': 3, 'Close Price': 160000, 'Above Grade Finished Area': 1600, 'Below Grade Finished Area': 600, 'Below Grade Unfinished Area': 200, 'Lot Size Square Feet': 6000, 'Bathrooms Full': 2, 'Bathrooms Half': 1, 'Garage Spaces': 2},
        {'Listing Id': 4, 'Close Price': 150000, 'Above Grade Finished Area': 1800, 'Below Grade Finished Area': 650, 'Below Grade Unfinished Area': 250, 'Lot Size Square Feet': 6500, 'Bathrooms Full': 2, 'Bathrooms Half': 1, 'Garage Spaces': 2},
        {'Listing Id': 5, 'Close Price': 140000, 'Above Grade Finished Area': 1400, 'Below Grade Finished Area': 700, 'Below Grade Unfinished Area': 300, 'Lot Size Square Feet': 7000, 'Bathrooms Full': 2, 'Bathrooms Half': 1, 'Garage Spaces': 2},
    ]
    df = pd.DataFrame(data)

    matched_columns = ['Close Price', 'Above Grade Finished Area', 'Below Grade Finished Area', 'Below Grade Unfinished Area',
                       'Lot Size Square Feet', 'Bathrooms Full', 'Bathrooms Half', 'Garage Spaces']
    tolerances = {'Close Price': 5000, 'Above Grade Finished Area': 200, 'Below Grade Finished Area': 50,
                  'Below Grade Unfinished Area': 50, 'Lot Size Square Feet': 1000, 'Bathrooms Full': 1, 'Bathrooms Half': 1,
                  'Garage Spaces': 1}

    # Find matches
    matches = compare_rows(df, matched_columns)

    # Verify that matches were found
    assert len(matches) > 0

    # Find matching pairs
    grouped_matches = match_pairs(df, matched_columns, matches)

    # Verify that matching pairs were found
    assert len(grouped_matches) > 0

    # Verify that a pair with an "Above Grade Finished Area" difference was found
    assert 'Above Grade Finished Area' in grouped_matches.keys()
    pairs = grouped_matches['Above Grade Finished Area']
    assert len(pairs) == 1
    pair = pairs[0]
    assert pair[0] == 1
    assert pair[1] == 2
    assert pair[2]


        
if __name__ == '__main__':
    unittest.main()           
