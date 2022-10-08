# Wrapper for the Oura Sleep Ring API
# Make sure that you have a Personal Access Token, which can be created on the Oura website.

# From the Oura website:
#   If you are using an existing OAuth2 library, you may need to configure the following URLs.
#   Authorize: https://cloud.ouraring.com/oauth/authorize
#   Access Token URL: https://api.ouraring.com/oauth/token

import requests
import pandas as pd


def get_user_info(personal_access_token: str):
    """Request basic user info associated with your PAT"""

    user_info = requests.get(f'https://api.ouraring.com/v1/userinfo?access_token={personal_access_token}')

    return print(user_info.json())


def get_sleep_data(personal_access_token: str, start_date: str, end_date: str):
    """Request sleep data"""

    print('Requesting sleep data... ', end='')

    sleep_data_request = requests.get(
        f'https://api.ouraring.com/v1/sleep?start={start_date}&end={end_date}&access_token={personal_access_token}')

    # Convert the response to JSON and read it into a data frame
    sleep_data_json = sleep_data_request.json()['sleep']
    sleep_df = pd.DataFrame.from_dict(sleep_data_json, orient='columns')

    print('done!')

    return sleep_df


def get_activity_data(personal_access_token: str, start_date: str, end_date: str):
    """Request activity data"""

    print('Requesting activity data... ', end='')

    activity_data_request = requests.get(
        f'https://api.ouraring.com/v1/activity?start={start_date}&end={end_date}&access_token={personal_access_token}')

    # Convert the response to JSON and read it into a data frame
    activity_data_json = activity_data_request.json()["activity"]
    activity_df = pd.DataFrame.from_dict(activity_data_json, orient="columns")

    print('done!')

    return activity_df


def get_readiness_data(personal_access_token: str, start_date: str, end_date: str):
    """Request readiness data"""

    print('Requesting readiness data... ', end='')

    readiness_data_request = requests.get(
        f'https://api.ouraring.com/v1/readiness?start={start_date}&end={end_date}&access_token={personal_access_token}')

    # Convert the response to JSON and read it into a data frame
    readiness_data_json = readiness_data_request.json()['readiness']
    readiness_df = pd.DataFrame.from_dict(readiness_data_json, orient='columns')

    print('done!')

    return readiness_df


def get_bedtime_data():
    """Request bedtime data"""

    print('Requesting bedtime data... ', end='')

    bedtime_data_request = requests.get(
        f'https://api.ouraring.com/v1/bedtime?start={start_date}&end={end_date}&access_token={personal_access_token}')

    # Convert the response to JSON and read it into a data frame
    bedtime_data_json = bedtime_data_request.json()['ideal_bedtimes']
    bedtime_df = pd.DataFrame.from_dict(bedtime_data_json, orient='columns')

    print('done!')

    return bedtime_df


def merge_all_to_full(sleep_df: pd.DataFrame, activity_df: pd.DataFrame, readiness_df: pd.DataFrame,
                      bedtime_df: pd.DataFrame):
    """Merges all 4 data frames (sleep, activity, readiness, bedtime) into one data frame"""

    print('Merging all four data sets... ', end='')

    # The key date column for each data frame is:
    # 'summary_date' for sleep_df, activity_df and readiness_df
    # 'date' for bedtime_df

    # To make it easier to identify the columns, add a prefix
    sleep_df = sleep_df.add_prefix('sleep.')
    activity_df = activity_df.add_prefix('activity.')
    readiness_df = readiness_df.add_prefix('readiness.')
    bedtime_df = bedtime_df.add_prefix('bedtime.')

    # Left join the four data frames (sleep, activity, readiness, bedtime)
    merged_1 = pd.merge(left=sleep_df, right=activity_df,
                        how='left',
                        left_on='sleep.summary_date', right_on='activity.summary_date')
    merged_2 = pd.merge(left=merged_1, right=readiness_df,
                        how='left',
                        left_on='sleep.summary_date', right_on='readiness.summary_date')
    full_df = pd.merge(left=merged_2, right=bedtime_df,
                       how='left',
                       left_on='sleep.summary_date', right_on='bedtime.date')

    # Then we can rename the key column 'sleep.summary_date' to just 'summary_date'
    full_df.rename(columns={'sleep.summary_date': 'summary_date'}, inplace=True)
    del full_df['bedtime.date']

    print('done!')

    return full_df


def get_short_dataset(full_df: pd.DataFrame):
    """Create a shortened version of the full dataset"""

    print('Creating a shortened version... ', end='')

    short_df = full_df[['summary_date',
                        'sleep.period_id',  # If there are more than one sleep period for a day (e.g. naps)
                        'sleep.is_longest', # Identifies the longest sleep period (night) from shorter ones (naps)
                        'sleep.deep',
                        'sleep.bedtime_start',
                        'sleep.bedtime_end',
                        'sleep.duration',
                        'sleep.total',
                        'sleep.awake',
                        'sleep.rem',
                        'sleep.light',
                        'sleep.deep',
                        'sleep.hr_lowest',
                        'sleep.hr_average',
                        'sleep.efficiency',
                        'sleep.onset_latency',
                        'sleep.restless',  # Percentage of sleep time during which the user was moving.
                        'sleep.temperature_delta',
                        'sleep.breath_average',
                        'sleep.score',  # Sleep score represents overall sleep quality during the sleep period.
                        'sleep.rmssd',  # The average HRV calculated with rMSSD method. Unit: milliseconds
                        'activity.score',
                        'activity.daily_movement',  # Daily physical activity as equal meters (walking meters).
                        'activity.non_wear',  # Number of minutes during the day when the user was not wearing the ring.
                        'activity.rest',
                        'activity.inactive',
                        'activity.low',
                        'activity.medium',
                        'activity.high',
                        'activity.steps',
                        'activity.cal_total',
                        'activity.cal_active',
                        'readiness.period_id',  # Index of the sleep period where 0 = first sleep period of the day
                        'readiness.score',
                        ]]

    print('done!')

    return short_df


if __name__ == '__main__':

    # For example:

    # Insert your Personal Access Token here
    PERSONAL_ACCESS_TOKEN = 'YOUR_PERSONAL_ACCESS_TOKEN_HERE'

    # Insert the time period for which you want to request your data. Format: 'YYYY-MM-DD'
    START_DATE = '2021-01-01'
    END_DATE = '2021-01-01'

    get_user_info(PERSONAL_ACCESS_TOKEN)

    sleep_df = get_sleep_data(PERSONAL_ACCESS_TOKEN, START_DATE, END_DATE)
    activity_df = get_activity_data(PERSONAL_ACCESS_TOKEN, START_DATE, END_DATE)
    readiness_df = get_readiness_data(PERSONAL_ACCESS_TOKEN, START_DATE, END_DATE)
    bedtime_df = get_bedtime_data(PERSONAL_ACCESS_TOKEN, START_DATE, END_DATE)

    full_df = merge_all_to_full(sleep_df, activity_df, readiness_df, bedtime_df)
    full_df.to_csv('full_df.csv', index=False, encoding='utf-8-sig')
    
    short_df = get_short_dataset(full_df)
    short_df.to_csv('short_df.csv', index=False, encoding='utf-8-sig')
