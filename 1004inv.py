import pandas as pd
from datetime import datetime, timedelta



def process_data():
    all_sales_filename = "all_sales.csv"
    competing_filename = "competing.csv"

    # Read in the csv files and create dataframes
    all_sales_df = pd.read_csv(all_sales_filename, na_values=[''])
    competing_df = pd.read_csv(competing_filename, na_values=[''])

    # Fill blank cells with 0
    all_sales_df.fillna(0, inplace=True)
    competing_df.fillna(0, inplace=True)

    # Convert dates to Unix timestamps
    all_sales_df['Listing Contract Date'] = (pd.to_datetime(all_sales_df['Listing Contract Date']) - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    all_sales_df['Purchase Contract Date'] = (pd.to_datetime(all_sales_df['Purchase Contract Date']) - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    all_sales_df['Close Date'] = (pd.to_datetime(all_sales_df['Close Date']) - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    competing_df['Listing Contract Date'] = (pd.to_datetime(competing_df['Listing Contract Date']) - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    competing_df['Purchase Contract Date'] = (pd.to_datetime(competing_df['Purchase Contract Date']) - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    competing_df['Close Date'] = (pd.to_datetime(competing_df['Close Date']) - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

    #get_recently_sold(competing_df)
    return competing_df


def get_recently_sold(competing_df):
    # Get the close dates and convert them to datetime objects
    close_dates = pd.to_datetime(competing_df['Close Date'], unit='s')

    # Find the dates that are between 365 and 180 days ago from today
    today = datetime.now()
    recent_dates_1 = [d for d in close_dates if (today - d).days >= 180 and (today - d).days <= 365]
    recent_dates_2 = [d for d in close_dates if (today - d).days >= 91 and (today - d).days <= 180]
    recent_dates_3 = [d for d in close_dates if (today - d).days >= 0 and (today - d).days <= 90]

    # Get the count of recently sold properties in each range
    count_1 = len(recent_dates_1)
    count_2 = len(recent_dates_2)
    count_3 = len(recent_dates_3)

    # Print the recent data to the console
    print("Recent sales data:")
    print("-------------------")
    print("Properties sold in the last 7-12 months:")
    for d in recent_dates_1:
        print(d.date())
    print("-------------------")
    print("Properties sold in the last 3-6 months:")
    for d in recent_dates_2:
        print(d.date())
    print("-------------------")
    print("Properties sold in the last 0-3 months:")
    for d in recent_dates_3:
        print(d.date())
    print("-------------------")

    # Print the count of recently sold properties in each range
    print(f"Number of properties sold in the last 7-12 months: {count_1}")
    print(f"Number of properties sold in the last 3-6 months: {count_2}")
    print(f"Number of properties sold in the last 0-3 months: {count_3}")

    # Create a dictionary with the counts of recently sold properties in each range
    counts_dict = {
        "7_12_sold": count_1,
        "4_6_sold": count_2,
        "0_3_sold": count_3
    }

    return counts_dict


""" def sold_in_last_12_months(competing_df):
    # Get the close dates and convert them to datetime objects
    close_dates = pd.to_datetime(competing_df['Close Date'], unit='s')

    # Calculate the start date for each period
    today = datetime.now()
    start_dates = []
    for i in range(0, 12):
        end_date = today - datetime.timedelta(days=365 - (30 * i))
        start_dates.append(end_date - datetime.timedelta(days=30))

    # Calculate the count of properties sold in each period
    counts = [0] * 12
    for date in close_dates:
        for i in range(0, 12):
            if date.date() > start_dates[i] and date.date() <= start_dates[i] + datetime.timedelta(days=30):
                counts[i] += 1
                break

    # Print the counts to the console
    print("Properties sold in the last 12 months, broken down into 30-day periods:")
    print("-----------------------------------------------------------------------")
    for i in range(0, 12):
        start_date = start_dates[i].strftime('%m/%d/%Y')
        end_date = (start_dates[i] + datetime.timedelta(days=30)).strftime('%m/%d/%Y')
        print(f"Properties sold between {start_date} and {end_date}: {counts[i]}")

    # Create a dictionary with the counts of properties sold in each period
    sold_counts_dict = {}
    for i in range(0, 12):
        key = f"{start_dates[i].strftime('%m/%d/%Y')}-{(start_dates[i] + datetime.timedelta(days=30)).strftime('%m/%d/%Y')}"
        sold_counts_dict[key] = counts[i]

    return sold_counts_dict """


def absorption_rate(counts_dict):
    # Define the constant factor for each range
    factor_1 = 6
    factor_2 = 3
    factor_3 = 3

    # Calculate the absorption rate for each range
    output_1 = counts_dict['7_12_sold'] / factor_1
    output_2 = counts_dict['4_6_sold'] / factor_2
    output_3 = counts_dict['0_3_sold'] / factor_3

    # Create a new dictionary with the absorption rate for each range
    absorb_dict = {
        "7_12_absorb": output_1,
        "4_6_absorb": output_2,
        "0_3_absorb": output_3
    }

    # Print the absorption rate for each range
    print("Absorption rate data:")
    print("---------------------")
    print(f"Absorption rate for properties sold in the last 7-12 months: {output_1}")
    print(f"Absorption rate for properties sold in the last 4-6 months: {output_2}")
    print(f"Absorption rate for properties sold in the last 0-3 months: {output_3}")
    print("---------------------")

    return absorb_dict

def active_listings(competing_df):
    # Get the listing dates and convert them to datetime objects
    listing_dates = pd.to_datetime(competing_df['Listing Contract Date'], unit='s')

    # Find the dates that are between 365 and 180 days ago from today
    today = datetime.now()
    recent_dates_1 = [d for d in listing_dates if (today - d).days >= 180 and (today - d).days <= 365]

    # Find the dates that are between 180 and 90 days ago from today
    recent_dates_2 = [d for d in listing_dates if (today - d).days >= 90 and (today - d).days <= 180]

    # Find the dates that are between 90 and 0 days ago from today
    recent_dates_3 = [d for d in listing_dates if (today - d).days >= 0 and (today - d).days <= 90]

    # Get the count of active listings in each range
    count_1 = 0
    for d in recent_dates_1:
        if len(competing_df[(competing_df['Listing Contract Date'] == d.timestamp()) & ((competing_df['Purchase Contract Date'] == 0) | (competing_df['Purchase Contract Date'] < (today - timedelta(days=180)).timestamp()))]) > 0:
            continue
        count_1 += 1

    count_2 = 0
    for d in recent_dates_2:
        if len(competing_df[(competing_df['Listing Contract Date'] == d.timestamp()) & ((competing_df['Purchase Contract Date'] == 0) | (competing_df['Purchase Contract Date'] < (today - timedelta(days=90)).timestamp()))]) > 0:
            continue
        count_2 += 1

    count_3 = 0
    for d in recent_dates_3:
        if len(competing_df[(competing_df['Listing Contract Date'] == d.timestamp()) & ((competing_df['Purchase Contract Date'] == 0) | (competing_df['Purchase Contract Date'] < today.timestamp()))]) > 0:
            continue
        count_3 += 1

    # Print the active listing data to the console
    print("Active listing data:")
    print("--------------------")
    print("Properties listed in the last 7-12 months:")
    for d in recent_dates_1:
        print(d.date())
    print("--------------------")
    print("Properties listed in the last 3-6 months:")
    for d in recent_dates_2:
        print(d.date())
    print("--------------------")
    print("Properties listed in the last 0-3 months:")
    for d in recent_dates_3:
        print(d.date())
    print("--------------------")

    # Print the count of active listings in each range
    print(f"Number of properties listed in the last 7-12 months: {count_1}")
    print(f"Number of properties listed in the last 3-6 months: {count_2}")
    print(f"Number of properties listed in the last 0-3 months: {count_3}")

    # Create a dictionary with the counts of active listings in each range
    counts_dict = {
        "7_12_listed": count_1,
        "4_6_listed": count_2,
        "0_3_listed": count_3
    }

    return counts_dict

def housing_supply(counts_dict):
    # Define the constant factor for each range
    factor_1 = 6
    factor_2 = 3
    factor_3 = 3

    # Calculate the housing supply absorption rate for each range
    result_1 = counts_dict['7_12_listed'] / factor_1
    result_2 = counts_dict['4_6_listed'] / factor_2
    result_3 = counts_dict['0_3_listed'] / factor_3

    # Print the count of active listings in each range
    print(f"Houseing supply absorption in the last 7-12 months: {result_1}")
    print(f"Houseing supply absorption in the last 3-6 months: {result_2}")
    print(f"Houseing supply absorption in the last 0-3 months: {result_3}")

    # Create a new dictionary with the housing supply absorption rate for each range
    housing_supply_dict = {
        "7_12_hs_ab": result_1,
        "4_6_hs_ab": result_2,
        "0_3_hs_ab": result_3
    }

    return housing_supply_dict





def main():
    competing_df = process_data()
    recent_sold_dict = get_recently_sold(competing_df)
    absorption_dict = absorption_rate(recent_sold_dict)
    active_listings_dict = active_listings(competing_df)
    housing_supply_dict = housing_supply(active_listings_dict)
    #sold_counts_dict = sold_in_last_12_months(competing_df)

    

__name__ == "__main__" and main()














    






   








