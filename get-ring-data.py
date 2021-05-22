# Some basic tools for working with the Oura Sleep Ring API.
# Make sure that you use your own Personal Access Token, which can be created
# on the Oura website.

# Import required modules
import requests
import json
import pandas as pd


# From the Oura website:
#   If you are using an existing OAuth2 library, you may need to configure the following URLs.
#   Authorize: https://cloud.ouraring.com/oauth/authorize
#   Access Token URL: https://api.ouraring.com/oauth/token


# Paste your Personal Access Token here inside quotation marks
personal_access_token = 'YOURPERSONALACCESSTOKENHERE'

# Insert time period for which you want to request your data
# Format: 'YYYY-MM-DD'
# For example: '2020-02-15'
# Tip: The start date can be earlier than when you started using the Ring
start_date = '2019-10-01'
end_date = '2021-03-10'

# Root endpoint for the API
root_endpoint = 'https://api.ouraring.com'

# Optional: get basic user info with your PAT
user_info = requests.get('https://api.ouraring.com/v1/userinfo?access_token={0}'.format(personal_access_token))

# Optional: Print the status code of this request
print(user_info.status_code)

# Print the request as JSON
print(user_info.json())


# Now the actual data requests

# 1. Sleep Data
# Request sleep data
sleep_data_request = requests.get(
    'https://api.ouraring.com/v1/sleep?start={0}&end={1}&access_token={2}'.format(start_date, end_date,
                                                                                  personal_access_token))

# Convert the response to JSON, read it into a data frame, and print to CSV
sleep_data_json = sleep_data_request.json()['sleep']
sleep_df = pd.DataFrame.from_dict(sleep_data_json, orient='columns')
sleep_df.to_csv('sleep.csv')


# 2. Activity Data
# Request activity data
activity_data_request = requests.get(
    'https://api.ouraring.com/v1/activity?start={0}&end={1}&access_token={2}'.format(start_date, end_date,
                                                                                     personal_access_token))

# Convert the response to JSON, read it into a data frame, and print to CSV
activity_data_json = activity_data_request.json()["activity"]
activity_df = pd.DataFrame.from_dict(activity_data_json, orient="columns")
activity_df.to_csv("activity.csv")


# 3. Readiness Data
# Request readiness data
readiness_data_request = requests.get(
    'https://api.ouraring.com/v1/readiness?start={0}&end={1}&access_token={2}'.format(start_date, end_date,
                                                                                      personal_access_token))

# Convert the response to JSON, read it into a data frame, and print to CSV
readiness_data_json = readiness_data_request.json()['readiness']
readiness_df = pd.DataFrame.from_dict(readiness_data_json, orient='columns')
readiness_df.to_csv('readiness.csv')


# 4. Bedtime data
# Request bedtime data
bedtime_data_request = requests.get(
    'https://api.ouraring.com/v1/bedtime?start={0}&end={1}&access_token={2}'.format(start_date, end_date,
                                                                                    personal_access_token))

# Convert the response to JSON, read it into a data frame, and print to CSV
bedtime_data_json = bedtime_data_request.json()['ideal_bedtimes']
bedtime_df = pd.DataFrame.from_dict(bedtime_data_json, orient='columns')
bedtime_df.to_csv('bedtime.csv')


# Next we merge the 3 (sleep/activity/readiness) data frames into one big data frame

# The key date column for each data frame is:
# 'summary_date' for sleep_df, activity_df and readiness_df
# 'date' for bedtime_df

# To make it easier to identify the columns,
# let's add a prefix (sleep/activity/readiness) for all the columns in each data frame.
sleep_df = sleep_df.add_prefix('sleep.')
activity_df = activity_df.add_prefix('activity.')
readiness_df = readiness_df.add_prefix('readiness.')

# Left join the three data frames (sleep, activity, readiness)
merged_sleep_activity = pd.merge(left=sleep_df, right=activity_df,
                                 how='left',
                                 left_on='sleep.summary_date', right_on='activity.summary_date')
merged_df = pd.merge(left=merged_sleep_activity, right=readiness_df,
                                           how='left',
                                           left_on='sleep.summary_date', right_on='readiness.summary_date')

# Then we can rename the key column 'sleep.summary_date' to just 'summary_date'
merged_df.rename(columns={'sleep.summary_date': 'summary_date'}, inplace=True)

# This is now the full, merged data set including sleep, activity, and readiness data
merged_df.to_csv('combined.csv')


# Create the shortened version with only selected columns
short_df = merged_df[['summary_date',
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

short_df.to_csv('short.csv')
