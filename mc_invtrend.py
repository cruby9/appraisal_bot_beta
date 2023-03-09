import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def count_sales_by_month(file_path):
    # Read the competing.csv file into a pandas dataframe
    competing_df = pd.read_csv(file_path)

    # Convert the Close Date column to datetime objects
    competing_df['Close Date'] = pd.to_datetime(competing_df['Close Date'])

    # Get today's date
    today = datetime.today()

    # Calculate the start date (365 days ago)
    start_date = today - timedelta(days=365)
    start_date = datetime.fromtimestamp(start_date.timestamp())

    # Create a list of 12 periods, each 30 days long
    periods = [(start_date + timedelta(days=30*i), start_date + timedelta(days=30*(i+1))) for i in range(12)]

    # Initialize an empty dictionary to store the counts
    counts = {}

    # Iterate over the periods and count the number of sales that fall within each period
    for i, period in enumerate(periods):
        start = period[0]
        end = period[1]
        mask = (competing_df['Close Date'] >= start) & (competing_df['Close Date'] < end)
        counts[i+1] = len(competing_df.loc[mask])

        # Print the sales count data to the console
    print("sales count:")
    print("--------------------")
    for i, period in enumerate(periods):
        print(f"Sales from {period[0].date()} to {period[1].date()}: {counts[i+1]}")
        print("--------------------")

    # Convert the dictionary to a pandas series
    counts_series = pd.Series(counts)

    # Calculate the slope of the counts data using numpy.polyfit
    X = counts_series.index
    Y = counts_series.values
    m, b = np.polyfit(X, Y, 1)

    # Store the counts and slope in a dictionary
    results = {'counts': counts_series, 'slope': m}
    print('slope:', m.round(2))

    # Return the results dictionary
    return results

def count_listings_by_month(competing_df):
    # Get the listing dates and convert them to datetime objects
    competing_df['Listing Contract Date'] = pd.to_datetime(competing_df['Listing Contract Date'], errors='coerce')
    competing_df['Purchase Contract Date'] = pd.to_datetime(competing_df['Purchase Contract Date'], errors='coerce')

    # Calculate the start date (long time ago)
    start_date = datetime.now() - timedelta(days=365)

    # Create a list of 12 periods, each 30 days long
    periods = [(start_date + timedelta(days=30*i), start_date + timedelta(days=30*(i+1))) for i in range(12)]

    # Initialize a dictionary to store the counts and listing IDs of active listings in each period
    counts_dict = {}
    listings_dict = {}

    # Initialize a list to store the listing IDs of purchased listings
    prev_purchases = []

    # Iterate over the periods and count the number of active listings that fall within each period
    for i, period in enumerate(periods):
        start = period[0]
        end = period[1]

        mask = ((competing_df['Listing Contract Date'] <= end) &
                ((competing_df['Purchase Contract Date'].isnull()) | 
                 (competing_df['Purchase Contract Date'] >= end)) &
                (competing_df['Listing Contract Date'] <= end))

        period_listings = competing_df.loc[mask]
        counts_dict[i+1] = len(period_listings)
        listings_dict[i+1] = list(period_listings['Listing Id'])

    # Print the active listing data to the console
    print("Active listing data:")
    print("--------------------")
    for i, period in enumerate(periods):
        print(f"Properties listed between {period[0].date()} and {period[1].date()}: {counts_dict[i+1]}")
        print(f"Listing Ids: {listings_dict[i+1]}")
        print("--------------------")
        print(f"End of period: {period[1].date()}")

    # Calculate the percent change over the 12 month period as the slope of a linear regression
    x = np.arange(1, len(periods)+1)
    y = list(counts_dict.values())
    m, b = np.polyfit(x, y, 1)
    percent_change = m.round(2)
    print(f"Percent change over 12 month period: {percent_change}%")
    return counts_dict

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def median_close_price_by_month(file_path):
    # Read the file into a pandas dataframe
    df = pd.read_csv(file_path)
    
    # Replace infinite and NaN values with 0
    df = df.replace([np.inf, -np.inf, np.nan], 0)
    
    # Convert the Close Date column to datetime objects
    df['Close Date'] = pd.to_datetime(df['Close Date'])

    # Get today's date
    today = datetime.today()

    # Calculate the start date (365 days ago)
    start_date = today - timedelta(days=365)
    start_date = datetime.fromtimestamp(start_date.timestamp())

    # Create a list of 12 periods, each 30 days long
    periods = [(start_date + timedelta(days=30*i), start_date + timedelta(days=30*(i+1))) for i in range(12)]

    # Initialize an empty dictionary to store the median close prices
    medians = {}

    # Iterate over the periods and find the median close price for each period
    for i, period in enumerate(periods):
        start = period[0]
        end = period[1]
        mask = (df['Close Date'] >= start) & (df['Close Date'] < end)
        median_close_price = df.loc[mask, 'Close Price'].median()
        if np.isnan(median_close_price):
            median_close_price = 0
            print(f"Median close price from {start.date()} to {end.date()} is NaN, replaced with 0")
        medians[i+1] = median_close_price

        # Print the median close price data to the console
        print("--------------------")
        print(f"Median close price from {start.date()} to {end.date()}: ${median_close_price:.2f}")

    # Convert the dictionary to a pandas series
    medians_series = pd.Series(medians)

    # Calculate the slope of the median close prices using numpy.polyfit
    X = medians_series.index
    Y = medians_series.values
    m, b = np.polyfit(X, Y, 1)

    # Store the median close prices and slope in a dictionary
    results = {'medians': medians_series, 'slope': m}
    print("--------------------")
    print(f"Slope of median close prices: {m:.2f}")

    # Return the results dictionary
    return results



import pandas as pd
from datetime import datetime, timedelta
import numpy as np

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def median_days_in_mls_by_month(file_path):
    # Read the file into a pandas dataframe
    df = pd.read_csv(file_path)
    
    # Replace infinite and NaN values with 0
    df = df.replace([np.inf, -np.inf, np.nan], 0)
    
    # Convert the Close Date column to datetime objects
    df['Close Date'] = pd.to_datetime(df['Close Date'])

    # Get today's date
    today = datetime.today()

    # Calculate the start date (365 days ago)
    start_date = today - timedelta(days=365)
    start_date = datetime.fromtimestamp(start_date.timestamp())

    # Create a list of 12 periods, each 30 days long
    periods = [(start_date + timedelta(days=30*i), start_date + timedelta(days=30*(i+1))) for i in range(12)]

    # Initialize an empty dictionary to store the median days in MLS
    medians = {}

    # Iterate over the periods and find the median days in MLS for each period
    for i, period in enumerate(periods):
        start = period[0]
        end = period[1]
        mask = (df['Close Date'] >= start) & (df['Close Date'] < end)
        median_days_in_mls = df.loc[mask, 'Days In MLS'].median()
        if np.isnan(median_days_in_mls):
            median_days_in_mls = 0
            print(f"Median days in MLS from {start.date()} to {end.date()} is NaN, replaced with 0")
        medians[i+1] = median_days_in_mls

        # Print the median days in MLS data to the console
        print("--------------------")
        print(f"Median days in MLS from {start.date()} to {end.date()}: {median_days_in_mls:.2f}")

    # Convert the dictionary to a pandas series
    medians_series = pd.Series(medians)

    # Calculate the slope of the median days in MLS using numpy.polyfit
    X = medians_series.index
    Y = medians_series.values
    m, b = np.polyfit(X, Y, 1)

    # Store the median days in MLS and slope in a dictionary
    results = {'medians': medians_series, 'slope': m}
    print("--------------------")
    print(f"Slope of median days in MLS: {m:.2f}")

    # Return the results dictionary
    return results

 
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def count_listings_by_month(competing_df):
    # Get the listing dates and convert them to datetime objects
    competing_df['Listing Contract Date'] = pd.to_datetime(competing_df['Listing Contract Date'], errors='coerce')
    competing_df['Purchase Contract Date'] = pd.to_datetime(competing_df['Purchase Contract Date'], errors='coerce')

    # Calculate the start date (long time ago)
    start_date = datetime.now() - timedelta(days=365)

    # Create a list of 12 periods, each 30 days long
    periods = [(start_date + timedelta(days=30*i), start_date + timedelta(days=30*(i+1))) for i in range(12)]

    # Initialize a dictionary to store the counts, listing IDs, and median list prices of active listings in each period
    counts_dict = {}
    listings_dict = {}
    medians_dict = {}

    # Initialize a list to store the listing IDs of purchased listings
    prev_purchases = []

    # Iterate over the periods and count the number of active listings that fall within each period
    for i, period in enumerate(periods):
        start = period[0]
        end = period[1]

        mask = ((competing_df['Listing Contract Date'] <= end) &
                ((competing_df['Purchase Contract Date'].isnull()) | 
                 (competing_df['Purchase Contract Date'] >= end)) &
                (competing_df['Listing Contract Date'] <= end))

        period_listings = competing_df.loc[mask]
        counts_dict[i+1] = len(period_listings)
        listings_dict[i+1] = list(period_listings['Listing Id'])
        medians_dict[i+1] = period_listings['List Price'].median()

    # Print the active listing data to the console
    print("Active listing data:")
    print("--------------------")
    for i, period in enumerate(periods):
        print(f"Properties listed between {period[0].date()} and {period[1].date()}: {counts_dict[i+1]}")
        print(f"Listing Ids: {listings_dict[i+1]}")
        print(f"Median list price: ${medians_dict[i+1]:,.2f}")
        print("--------------------")
        print(f"End of period: {period[1].date()}")

    # Calculate the percent change over the 12 month period as the slope of a linear regression
    x = np.arange(1, len(periods)+1)
    y = list(counts_dict.values())
    m, b = np.polyfit(x, y, 1)
    percent_change = m.round(2)
    print(f"Percent change over 12 month period: {percent_change}%")

    # Return the counts, listing IDs, and median list prices as dictionaries
    return {'counts': counts_dict, 'listings': listings_dict, 'medians': medians_dict}

import pandas as pd
import numpy as np

def median_days_on_market_by_month(competing_df):
    # Get the listing dates and convert them to datetime objects
    competing_df['Listing Contract Date'] = pd.to_datetime(competing_df['Listing Contract Date'], errors='coerce')
    competing_df['Purchase Contract Date'] = pd.to_datetime(competing_df['Purchase Contract Date'], errors='coerce')

    # Calculate the start date (long time ago)
    start_date = datetime.now() - timedelta(days=365)

    # Create a list of 12 periods, each 30 days long
    periods = [(start_date + timedelta(days=30*i), start_date + timedelta(days=30*(i+1))) for i in range(12)]

    # Initialize a dictionary to store the median days on market of active listings in each period
    median_dict = {}

    # Iterate over the periods and calculate the median days on market for active listings that fall within each period
    for i, period in enumerate(periods):
        end = period[1]

        mask = ((competing_df['Listing Contract Date'] <= end) &
                ((competing_df['Purchase Contract Date'].isnull()) | 
                 (competing_df['Purchase Contract Date'] >= end)) &
                (competing_df['Listing Contract Date'] <= end))

        period_listings = competing_df.loc[mask]

        if len(period_listings) > 0:
            listing_dates = pd.to_datetime(period_listings['Listing Contract Date'], format='%m/%d/%Y')
            days_on_market = (end - listing_dates).dt.days
            median_days_on_market = int(days_on_market.median())
            median_dict[i+1] = median_days_on_market

            # Print the Listing Ids and listing dates being used for the calculation
            print(f"Listings for period {i+1} ({period[0].date()} to {period[1].date()}):")
            print(period_listings[['Listing Id', 'Listing Contract Date']])

            # Print the median days on market
            print(f"Median days on market for period {i+1}: {median_days_on_market}")
            print("------------------------------------")

    # Return the median days on market as a dictionary
    return median_dict

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def sale_to_list_ratio(file_path):
    # Read the file into a pandas dataframe
    df = pd.read_csv(file_path)
    
    # Replace infinite and NaN values with 0
    df = df.replace([np.inf, -np.inf, np.nan], 0)
    
    # Convert the Close Date column to datetime objects
    df['Close Date'] = pd.to_datetime(df['Close Date'])

    # Get today's date
    today = datetime.today()

    # Calculate the start date (365 days ago)
    start_date = today - timedelta(days=365)
    start_date = datetime.fromtimestamp(start_date.timestamp())

    # Create a list of 12 periods, each 30 days long
    periods = [(start_date + timedelta(days=30*i), start_date + timedelta(days=30*(i+1))) for i in range(12)]

    # Initialize an empty list to store the sale-to-list ratios
    ratios = []

    # Iterate over the periods and calculate the sale-to-list ratio for each property in the period
    for i, period in enumerate(periods):
        start = period[0]
        end = period[1]
        mask = (df['Close Date'] >= start) & (df['Close Date'] < end)
        period_df = df.loc[mask]
        period_ratios = period_df['Close Price'] / period_df['List Price']
        period_ratios = period_ratios.dropna()
        period_ratios = period_ratios[period_ratios > 0]
        ratios.append(period_ratios)

        # Print the median sale-to-list ratio for the period, replacing NaN with 0
        median_ratio = period_ratios.median()
        if np.isnan(median_ratio):
            median_ratio = 0
            print(f"Median sale-to-list ratio from {start.date()} to {end.date()}: 0%")
        else:
            print(f"Median sale-to-list ratio from {start.date()} to {end.date()}: {median_ratio*100:.2f}%")

    # Convert the list of ratios to a pandas series
    ratios_series = pd.Series(ratios)

    # Flatten the series and calculate the overall median sale-to-list ratio
    flattened_ratios = ratios_series.explode()
    median_ratio = flattened_ratios.median()
    print("--------------------")
    print(f"Overall median sale-to-list ratio: {median_ratio*100:.2f}%")

    # Calculate the slope of the sale-to-list ratios using numpy.polyfit
    X = flattened_ratios.index.values.astype('float64')
    Y = flattened_ratios.values.astype('float64')
    valid_mask = np.isfinite(X) & np.isfinite(Y)
    if np.any(valid_mask):
        m, b = np.polyfit(X[valid_mask], Y[valid_mask], 1)
    else:
        m = np.nan
    print("--------------------")
    print(f"Slope of sale-to-list ratios: {m:.2f}")

    # Store the median sale-to-list ratios and slope in a dictionary
    results = {'medians': flattened_ratios, 'slope': m}

    # Return the results dictionary
    return results





if __name__ == '__main__':
    file_path = 'competing.csv'
    competing_df = pd.read_csv(file_path)

    count_sales_by_month(file_path)
    result = count_listings_by_month(competing_df)
    counts_dict = result['counts']
    listings_dict = result['listings']

    median_close_price_by_month(file_path)

    listing_contract_date_col = 'Listing Contract Date'
    result = median_days_in_mls_by_month(file_path)
    medians_series = result['medians']
    contract_date_col = 'Listing Contract Date'
    median_days_on_market_by_month(competing_df)

    print("\nSale-to-List Ratio by Month:")
    sale_to_list_ratios = sale_to_list_ratio(file_path)





