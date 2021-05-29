# Wrapper for the Oura Sleep Ring API
# Make sure that you have a Personal Access Token, which can be created
# on the Oura website.

# Import modules
import requests
import pandas as pd


# From the Oura website:
#   If you are using an existing OAuth2 library, you may need to configure the following URLs.
#   Authorize: https://cloud.ouraring.com/oauth/authorize
#   Access Token URL: https://api.ouraring.com/oauth/token


# Insert your Personal Access Token here
personal_access_token = 'YOURPERSONALACCESSTOKEN'

# Insert the time period for which you want to request your data
# Format: 'YYYY-MM-DD'
start_date = '2020-01-01'
end_date = '2021-03-15'


# Root endpoint for the API
root_endpoint = 'https://api.ouraring.com'


def get_user_info():
    """Request basic user info associated with your PAT"""

    user_info = requests.get('https://api.ouraring.com/v1/userinfo?access_token={0}'.format(personal_access_token))

    return print(user_info.json())


def save_to_csv(df, name_of_file):
    """Save a data set to CSV"""

    df.to_csv(name_of_file + '.csv')

    return


def get_sleep_data():
    """Request sleep data"""

    print('Requesting sleep data... ', end='')

    sleep_data_request = requests.get(
        'https://api.ouraring.com/v1/sleep?start={0}&end={1}&access_token={2}'.format(start_date, end_date,
                                                                                      personal_access_token))

    # Convert the response to JSON and read it into a data frame
    sleep_data_json = sleep_data_request.json()['sleep']
    sleep_df = pd.DataFrame.from_dict(sleep_data_json, orient='columns')

    print('done!')

    return sleep_df


def get_activity_data():
    """Request activity data"""

    print('Requesting activity data... ', end='')

    activity_data_request = requests.get(
        'https://api.ouraring.com/v1/activity?start={0}&end={1}&access_token={2}'.format(start_date, end_date,
                                                                                         personal_access_token))

    # Convert the response to JSON and read it into a data frame
    activity_data_json = activity_data_request.json()["activity"]
    activity_df = pd.DataFrame.from_dict(activity_data_json, orient="columns")

    print('done!')

    return activity_df


def get_readiness_data():
    """Request readiness data"""

    print('Requesting readiness data... ', end='')

    readiness_data_request = requests.get(
        'https://api.ouraring.com/v1/readiness?start={0}&end={1}&access_token={2}'.format(start_date, end_date,
                                                                                          personal_access_token))

    # Convert the response to JSON and read it into a data frame
    readiness_data_json = readiness_data_request.json()['readiness']
    readiness_df = pd.DataFrame.from_dict(readiness_data_json, orient='columns')

    print('done!')

    return readiness_df


def get_bedtime_data():
    """Request bedtime data"""

    print('Requesting bedtime data... ', end='')

    bedtime_data_request = requests.get(
        'https://api.ouraring.com/v1/bedtime?start={0}&end={1}&access_token={2}'.format(start_date, end_date,
                                                                                        personal_access_token))

    # Convert the response to JSON and read it into a data frame
    bedtime_data_json = bedtime_data_request.json()['ideal_bedtimes']
    bedtime_df = pd.DataFrame.from_dict(bedtime_data_json, orient='columns')

    print('done!')

    return bedtime_df


def merge_all():
    """Merges all 4 data sets (sleep, activity, readiness, bedtime) into one table"""

    print('Merging all four data sets... ', end='')

    global sleep_df, activity_df, readiness_df, bedtime_df

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


def get_shortened():
    """Create a shortened version of the full data set"""

    print('Creating a shortened version... ', end='')

    global full_df

    short_df = full_df[['summary_date',
                        'sleep.period_id',  # If there are more than one sleep period for a day (e.g. naps)
                        'sleep.is_longest',  # Identifies the longest sleep period (night) from shorter ones (naps)
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

    get_user_info()

    sleep_df = get_sleep_data()
    save_to_csv(sleep_df, 'sleep')
    
    activity_df = get_activity_data()
    
    readiness_df = get_readiness_data()
    
    bedtime_df = get_bedtime_data()
    
    full_df = merge_all()
    save_to_csv(full_df, 'full')
    
    short_df = get_shortened()
    save_to_csv(short_df, 'short')
