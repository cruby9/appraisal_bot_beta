import csv
from copy import deepcopy





""" def read_database_from_file(file_path):
    database = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            database.append(row)
    return database """

""" def process_data(database, column_names):
    for row in database:
        for column_name in column_names:
            if column_name in row:
                if row[column_name] == '':
                    row[column_name] = 0
                elif column_name in ['Below Grade Finished Area', 'Below Grade Unfinished Area', 
                                     'Lot Size Square Feet', 'Bathrooms Full', 'Bathrooms Half', 'Garage Spaces']:
                    try:
                        row[column_name] = int(float(row[column_name]))
                    except ValueError:
                        pass
                elif column_name == 'Above Grade Finished Area':
                    try:
                        row[column_name] = round(float(row[column_name]))
                    except ValueError:
                        pass
    return database """
def process_data(database, column_names):
    for row in database:
        for column_name in column_names:
            if column_name in row:
                if row[column_name] == '':
                    row[column_name] = 0
                elif column_name in ['Below Grade Finished Area', 'Below Grade Unfinished Area', 
                                     'Lot Size Square Feet', 'Bathrooms Full', 'Bathrooms Half', 'Garage Spaces']:
                    try:
                        row[column_name] = int(float(row[column_name]))
                    except ValueError:
                        pass
                elif column_name == 'Above Grade Finished Area':
                    try:
                        row[column_name] = round(float(row[column_name]))
                    except ValueError:
                        pass

    return database

def process_bathrooms(database):
    new_database = []
    for row in database:
        new_row = deepcopy(row)
        if new_row['Bathrooms Three Quarter']:
            new_row['Bathrooms Full'] = int(new_row['Bathrooms Full']) + int(new_row['Bathrooms Three Quarter'])
        if new_row['Bathrooms One Quarter']:
            new_row['Bathrooms Half'] = int(new_row['Bathrooms Half']) + int(new_row['Bathrooms One Quarter'])
        new_database.append(new_row)
    return new_database

def match_properties(database, new_database, column_names, tolerance_bgfa, tolerance_lssf, tolerance_agfa):
    paired_properties = []
    paired_listing_ids = set()
    
    for i in range(len(new_database)):
        for j in range(i + 1, len(new_database)):
            if (new_database[i]['Below Grade Finished Area'] >= new_database[j]['Below Grade Finished Area'] - tolerance_bgfa and
                new_database[i]['Below Grade Finished Area'] <= new_database[j]['Below Grade Finished Area'] + tolerance_bgfa and
                new_database[i]['Below Grade Unfinished Area'] >= new_database[j]['Below Grade Unfinished Area'] - tolerance_bgfa and
                new_database[i]['Below Grade Unfinished Area'] <= new_database[j]['Below Grade Unfinished Area'] + tolerance_bgfa and
                new_database[i]['Lot Size Square Feet'] >= new_database[j]['Lot Size Square Feet'] - tolerance_lssf and
                new_database[i]['Lot Size Square Feet'] <= new_database[j]['Lot Size Square Feet'] + tolerance_lssf and
                new_database[i]['Bathrooms Full'] == new_database[j]['Bathrooms Full'] and
                new_database[i]['Bathrooms Half'] == new_database[j]['Bathrooms Half'] and
                new_database[i]['Garage Spaces'] == new_database[j]['Garage Spaces'] and
                abs(new_database[i]['Above Grade Finished Area'] - new_database[j]['Above Grade Finished Area']) > tolerance_agfa and
                new_database[i]['Close Price'] != 0 and new_database[j]['Close Price'] != 0):
                paired_properties.append([new_database[i], new_database[j]])
                paired_listing_ids.add(new_database[i]['Listing Id'])
                paired_listing_ids.add(new_database[j]['Listing Id'])
    
    print("Paired Properties:")
    return paired_properties

   

""" def match_properties(database, column_names, tolerance_bgfa, tolerance_lssf, tolerance_agfa):
    paired_properties = []
    paired_listing_ids = set()
    
    #database = process_data(database, column_names)
    
    for i in range(len(database)):
        for j in range(i + 1, len(database)):
            if (database[i]['Below Grade Finished Area'] >= database[j]['Below Grade Finished Area'] - tolerance_bgfa and
                database[i]['Below Grade Finished Area'] <= database[j]['Below Grade Finished Area'] + tolerance_bgfa and
                database[i]['Below Grade Unfinished Area'] >= database[j]['Below Grade Unfinished Area'] - tolerance_bgfa and
                database[i]['Below Grade Unfinished Area'] <= database[j]['Below Grade Unfinished Area'] + tolerance_bgfa and
                database[i]['Lot Size Square Feet'] >= database[j]['Lot Size Square Feet'] - tolerance_lssf and
                database[i]['Lot Size Square Feet'] <= database[j]['Lot Size Square Feet'] + tolerance_lssf and
                database[i]['Bathrooms Full'] == database[j]['Bathrooms Full'] and
                database[i]['Bathrooms Half'] == database[j]['Bathrooms Half'] and
                database[i]['Garage Spaces'] == database[j]['Garage Spaces'] and
                abs(database[i]['Above Grade Finished Area'] - database[j]['Above Grade Finished Area']) > tolerance_agfa and
                database[i]['Close Price'] != 0 and database[j]['Close Price'] != 0):
                paired_properties.append([database[i], database[j]])
                paired_listing_ids.add(database[i]['Listing Id'])
                paired_listing_ids.add(database[j]['Listing Id'])
    
    print("Paired Properties:")
    return paired_properties """


def calculate_price_change_psf(pair):
    price_diff = abs(pair[0]['Close Price'] - pair[1]['Close Price'])
    agfa_diff = abs(pair[0]['Above Grade Finished Area'] - pair[1]['Above Grade Finished Area'])
    price_change_psf = price_diff / agfa_diff
    return price_diff, agfa_diff, round(price_change_psf, 0)

def test_match_properties():
    file_path = 'all_sales.csv'
    database = read_database_from_file(file_path)
    column_names = ['Below Grade Finished Area', 'Below Grade Unfinished Area', 'Lot Size Square Feet', 
                    'Bathrooms Full', 'Bathrooms Half', 'Garage Spaces', 'Above Grade Finished Area']
    tolerance_bgfa = 50
    tolerance_lssf = 1000.0
    tolerance_agfa = 50.0
    paired_properties = match_properties(database, column_names, tolerance_bgfa, tolerance_lssf, tolerance_agfa)
    if not paired_properties:
        print("No Paired Properties Found.")
    else:
        with open('paired_properties.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Pair Number', 'Listing Id 1', 'Above Grade Finished Area 1', 'Close Price 1', 
                             'Listing Id 2', 'Above Grade Finished Area 2', 'Close Price 2',
                             'Price Diff', 'GLA Diff', 'Price Change PSF'])
            pair_number = 1
            for pair in paired_properties:
                price_diff = float(pair[0]['Close Price']) - float(pair[1]['Close Price'])
                gla_diff = pair[0]['Above Grade Finished Area'] - pair[1]['Above Grade Finished Area']
                price_change_psf = price_diff / gla_diff if gla_diff != 0 else 0
                writer.writerow([pair_number, pair[0]['Listing Id'], pair[0]['Above Grade Finished Area'],
                                 pair[0]['Close Price'], pair[1]['Listing Id'], pair[1]['Above Grade Finished Area'],
                                 pair[1]['Close Price'], price_diff, gla_diff, price_change_psf])
                pair_number += 1


def read_database_from_file(file_path):
    database = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            for key, value in row.items():
                if value == '':
                    row[key] = 0
                elif key in ['Below Grade Finished Area', 'Below Grade Unfinished Area', 
                             'Lot Size Square Feet', 'Bathrooms Full', 'Bathrooms Half', 'Garage Spaces']:
                    try:
                        row[key] = int(float(value))
                    except ValueError:
                        pass
                elif key == 'Above Grade Finished Area':
                    try:
                        row[key] = round(float(value))
                    except ValueError:
                        pass
            database.append(row)
    return database





if __name__ == '__main__':
    test_match_properties()
new_database = combine_bathrooms(database)
paired_properties = match_properties(database, new_database, column_names, tolerance_bgfa, tolerance_lssf, tolerance_agfa)

file_path = 'all_sales.csv'
#database = read_database_from_file(file_path)
column_names = ['Below Grade Finished Area', 'Below Grade Unfinished Area', 'Lot Size Square Feet','Bathrooms Full', 'Bathrooms Half', 'Garage Spaces', 'Above Grade Finished Area']
tolerance_bgfa = 50
tolerance_lssf = 1000.0
tolerance_agfa = 50.0
#database = process_data(database, column_names, tolerance_bgfa, tolerance_lssf, tolerance_agfa)

                



