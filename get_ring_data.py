"""
Wrapper for the Oura Sleep Ring API v2.

Make sure that you have a Personal Access Token, which can be created on the Oura website.

From the Oura website:
    - If you are using an existing OAuth2 library, you may need to configure the following URLs.
    - Authorize: https://cloud.ouraring.com/oauth/authorize
    - Access Token URL: https://api.ouraring.com/oauth/token
"""

import requests
import pandas as pd


def request_user_info(personal_access_token: str):
    """Request basic user information associated with your PAT"""

    url = 'https://api.ouraring.com/v2/usercollection/personal_info'

    headers = {
        'Authorization': f'Bearer {personal_access_token}'
    }

    user_info = requests.request('GET', url, headers=headers, timeout=10)

    print(user_info.json())


def request_data(data_type: str,
                 personal_access_token: str,
                 start_date: str,
                 end_date: str):
    """Request data for a specific type.
    Choose from: sleep, daily_sleep, daily_activity, daily_readiness, sleep_time, tag,
    workout, session, daily_spo2, heartrate, rest_mode_period

    Parameters
    ----------
    data_type : str
        The type of data to request. Choose from: sleep, daily_sleep, daily_activity,
        daily_readiness, sleep_time, tag, workout, session, daily_spo2, heartrate, rest_mode_period
    personal_access_token : str
        Your personal access token
    start_date : str
        The start date for the data request. Format: 'YYYY-MM-DD'
    end_date : str
        The end date for the data request. Format: 'YYYY-MM-DD'
    """

    if data_type in ['sleep', 'daily_sleep', 'daily_activity', 'daily_readiness', 'sleep_time',
                     'tag', 'workout', 'session', 'daily_spo2', 'heartrate', 'rest_mode_period']:
        print(f'Requesting {data_type} data... ', end='')
        url = f'https://api.ouraring.com/v2/usercollection/{data_type}'
    else:
        print('Invalid data type. Please choose one from: sleep, daily_sleep, daily_activity, '
              'daily_readiness, sleep_time, tag, workout, session, daily_spo2, heartrate, '
              'rest_mode_period')
        return

    params = {
        'start_date': f'{start_date}',
        'end_date': f'{end_date}'
    }

    headers = {
        'Authorization': f'Bearer {personal_access_token}'
    }

    response = requests.request('GET', url, headers=headers, params=params, timeout=10)

    response_json = response.json()['data']
    response_df = pd.DataFrame.from_dict(response_json, orient='columns')

    print('done!')

    return response_df


def request_flat_data(data_type: str,
                      personal_access_token: str,
                      start_date: str,
                      end_date: str):
    """Request flattened data for a specific type.
    This flattens the 'contributors' column into separate columns for easier use and analysis.
    Choose from: daily_sleep, daily_activity, daily_readiness.

    Parameters
    ----------
    data_type : str
        The type of data to request. Choose from: daily_sleep, daily_activity, daily_readiness
    personal_access_token : str
        Your personal access token
    start_date : str
        The start date for the data request. Format: 'YYYY-MM-DD'
    end_date : str
        The end date for the data request. Format: 'YYYY-MM-DD'
    """

    if data_type in ['daily_sleep', 'daily_activity', 'daily_readiness']:
        print(f'Requesting flat {data_type} data... ', end='')
        url = f'https://api.ouraring.com/v2/usercollection/{data_type}'
    else:
        print('Invalid data type. Please choose one from: daily_sleep, daily_activity, '
              'daily_readiness')
        return

    params = {
        'start_date': f'{start_date}',
        'end_date': f'{end_date}'
    }

    headers = {
        'Authorization': f'Bearer {personal_access_token}'
    }

    response = requests.request('GET', url, headers=headers, params=params, timeout=10)

    response_json = response.json()['data']
    response_df = pd.DataFrame.from_dict(response_json, orient='columns')

    # Expand the 'contributors' column into separate columns
    contributors_df = pd.DataFrame(response_df['contributors'].values.tolist())
    contributors_df.columns = 'contributors.' + contributors_df.columns

    # Concatenate the original DataFrame with the expanded 'contributors' DataFrame
    result_df = pd.concat([response_df.drop(columns=['contributors']), contributors_df], axis=1)

    print('done!')

    return result_df


if __name__ == '__main__':
    # EXAMPLE CODE BELOW

    # Insert your Personal Access Token here
    PERSONAL_ACCESS_TOKEN = 'YOUR_PERSONAL_ACCESS_TOKEN'

    # Specify the time period for which you want to request your data. Format: 'YYYY-MM-DD'
    START_DATE = '2023-09-01'
    END_DATE = '2023-09-10'

    # Get basic user information
    request_user_info(PERSONAL_ACCESS_TOKEN)

    # Request data
    sleep_df = request_data('sleep', PERSONAL_ACCESS_TOKEN, START_DATE, END_DATE)
    daily_sleep_df = request_data('daily_sleep', PERSONAL_ACCESS_TOKEN, START_DATE, END_DATE)
    daily_activity_df = request_data('daily_activity', PERSONAL_ACCESS_TOKEN, START_DATE, END_DATE)

    # Request flattened data
    daily_sleep_flat_df = request_flat_data('daily_sleep', PERSONAL_ACCESS_TOKEN, START_DATE,
                                            END_DATE)

    # Save to CSV
    sleep_df.to_csv('sleep_df.csv', index=False, encoding='utf-8-sig')
    daily_sleep_flat_df.to_csv('daily_sleep_flat_df.csv', index=False, encoding='utf-8-sig')
