#this program is import the subject and comp data to prepare
#it to be parsed and printed to website

import pandas as pd
import numpy as np


# Load data from CSV file into a pandas DataFrame
df = pd.read_csv('subject.csv')

# Print the first 5 rows of the DataFrame
print(df.head())


df = pd.read_csv('subject.csv', header=0)


import pandas as pd

# Load data from CSV file into a pandas DataFrame
df = pd.read_csv('subject.csv')

# Concatenate two lines from the 'Address' column into a new column called 'Full Address'
df['Address'] = df['Street Number'].astype(str) + ' ' + df['Street Name'] + ' ' + df['Street Suffix'] + '\n' + df['City'] + ' ' + df['State Or Province'] + ' ' + df['Postal Code'].astype(str)

# Combine the 'Close Price' and 'List Price' columns and fill missing values with a default value of 100
df['Price'] = df['Close Price'].fillna(df['List Price']).fillna(100)




def get_sale_type(contingency, close_date):
    """
    Given a contingency value and close date, returns the corresponding abbreviation for the Sale Type column.
    """
    if pd.isnull(close_date):
        return "Listing"
    elif pd.isnull(contingency) or contingency == "":
        return "Armlth"
    elif contingency == "Offer accepted awaiting REO approval":
        return "REO"
    elif contingency == "Offer waiting on RELO company approval":
        return "Relo"
    elif contingency == "Short Sale - Have signed offer(s) waiting on lender approval" or contingency == "Short Sale - Have unsigned offer(s) waiting on lender approval":
        return "Short Sale"
    elif contingency == "Offer accepted contingent on court approval":
        return "Estate"
    else:
        return np.nan

import datetime

def to_unix_time(date_string):
    """
    Given a date string, returns a Unix timestamp representing the date.
    """
    if pd.isnull(date_string):
        return ""
    else:
        date = datetime.datetime.strptime(date_string, '%m/%d/%Y %I:%M:%S %p')
        return int(date.timestamp())



""" def format_date(date_str):
    if pd.isnull(date_str):
        return ''
    date = pd.to_datetime(date_str)
    return date.strftime('%b%y') """

""" def format_dates(df):
    close_date = df['Close Date'].apply(lambda x: pd.to_datetime(x, errors='coerce'))
    close_date = close_date.dropna().apply(lambda x: f's{x.month}/{str(x.year)[2:]}')
    listing_date = df['Listing Contract Date'].apply(lambda x: pd.to_datetime(x, errors='coerce'))
    listing_date = listing_date.dropna().apply(lambda x: f'c{x.month}/{str(x.year)[2:]}')
    date_str = ';'.join(filter(None, [close_date.to_string(index=False), listing_date.to_string(index=False)]))
    return pd.DataFrame({'Date': [date_str]}) """

"""def get_date(date, date_type):
    
    #Given a date, returns the month and year in the format mmyy.
    
    if pd.isna(date):
        return ""
    prefix = "s" if date_type == "Close Date" else "c"
    date = pd.to_datetime(date)
    return prefix + date.strftime("%m/%y")"""

def format_view(view):
    """
    Given a view string, returns a formatted abbreviation for the View column.
    """
    if pd.isnull(view) or view == "":
        return "N;Res;"
    else:
        view_dict = {"Mountain(s)": "Mnt", "City": "CtySky", "Meadow": "Pstrl", "Water": "Wtr"}
        view_list = [v.strip() for v in view.split(",")]
        formatted_list = ["N"]
        for v in view_list:
            if v in view_dict:
                formatted_list.append(view_dict[v])
        return ";".join(formatted_list)

def format_levels(levels, prop_sub_type, arch_style):
    """
    Given a levels string, property subtype, and architectural style,
    returns a formatted abbreviation for the Design (Style) column.
    """
    if prop_sub_type != 'Single Family Residence':
        return ''

    levels_dict = {
        'One': f"DT1;{'Ranch' if arch_style == '' else arch_style}",
        'Two': f"DT2;{'2Story' if arch_style == '' else arch_style}",
        'Multi/Split': f"DT2;{'SplitLevel' if arch_style == '' else arch_style}",
        'Bi-Level': f"DT2;{'Bilevel' if arch_style == '' else arch_style}",
        'Three Or More': f"DT3;{'3Story' if arch_style == '' else arch_style}"
    }

    if pd.isnull(levels) or levels == '':
        return levels_dict['One']
    else:
        return levels_dict.get(levels, '')

def add_baths_beds(df):
    """
    Given a DataFrame with 'Bathrooms Total Integer' and 'Bedrooms Total' columns,
    returns a new Series with the sum of these columns plus 2.
    """
    return df['Bathrooms Total Integer'] + df['Bedrooms Total'] + 2
df['total_room_count'] = add_baths_beds(df)

def total_rooms(df):
    """
    Given a DataFrame with 'Upper Level Bedrooms', 'Main Level Bedrooms', and 'Lower Level Bedrooms' columns,
    returns the sum of those columns plus 2.
    """
    return df['Upper Level Bedrooms'].fillna(0) + df['Main Level Bedrooms'].fillna(0) + df['Lower Level Bedrooms'].fillna(0) + 2

def bed_count(df):
    """
    Given a DataFrame with 'Upper Level Bedrooms', 'Main Level Bedrooms', and 'Lower Level Bedrooms' columns,
    returns the sum of those columns plus 2.
    """
    return df['Upper Level Bedrooms'].fillna(0) + df['Main Level Bedrooms'].fillna(0) + df['Lower Level Bedrooms'].fillna(0)

def baths_above(df):
    return df['Bathrooms Total Integer'].fillna(0) - df['Basement Level Bathrooms'].fillna(0) + \
           df['Bathrooms One Quarter'].fillna(0) * 0.1 + \
           df['Bathrooms Half'].fillna(0) * 0.1







# Create a new DataFrame with the desired columns
new_df = pd.DataFrame({
    'Address': df['Address'],
    'Price_Current_Sale': df['Price'],    
    'Data_source': ('MLS') + '#' + df['Listing Id'].astype(str) + ';' + ('DOM ') + df['Days In MLS'].astype(str),
    'Verification_Source': ('MLS/ Public Records'),
    'Sale_type': df.apply(lambda row: get_sale_type(row['Contingency'], row['Close Date']), axis=1).fillna('Armlth'),
    'Concessions': np.where(pd.isnull(df['Close Date']), '', df['Buyer Financing'].astype(str) + ';' + df['Concessions Amount'].fillna(0).astype(str)),
    'Date': df['Close Date'].apply(to_unix_time).astype(str) + ';' + df['Listing Contract Date'].apply(to_unix_time).astype(str),
    'Location': ('N;Res:;'),
    'Leasehold/Fee Simple': ('Fee Simple'),
    'Site': df['Lot Size Square Feet'].astype(str) + '' + 'sf',
    'View': df['View'].apply(format_view),
    'Design (Style)': df.apply(lambda row: format_levels(row['Levels'], row['Property Sub Type'], row['Architectural Style']), axis=1),
    'Quality': ('Q4'),
    'Actual Age': df['Year Built'],
    'Condition': ('Q3'),
    'Total_Room_Count': total_rooms(df),
    'Bedroom_count': bed_count(df),
    'Bathroom_count': baths_above(df),
    'Basement_bedroom': df['Basement Level Bedrooms'],
    'Basement _bathroom': df['Basement Level Bathrooms'], 
    'Above_Grade_GLA': df['Above Grade Finished Area'],
    'Basement_unfinished': df['Below Grade Unfinished Area'],
    'Basement_finished': df['Below Grade Finished Area'],
    'Functional Utility': ('Typical'),
    'Heating': df['Heating'],
    'Cooling': df['Cooling'],
    'Energy Efficient Items': ('None'),
    'Garage': df['Garage Spaces'],
    'Carport': df['Carport Spaces'],
    'Porch/Patio/Deck': df['Patio And Porch Features'],
    'Fireplaces': df['Fireplaces Total']
})

# Print the first 5 rows of the new DataFrame
pd.set_option('display.max_columns', None)
print(new_df)
