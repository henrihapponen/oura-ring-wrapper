# Oura-Ring-API-Wrapper

This script is an attempt to provide some useful tools that make it easier to work with the Oura Ring API.

The API documentation on Oura's website provides very little guidance, with some sections lacking documentation altogether, which is why I created this project. I hope this is helpful for anyone who wants to download and analyse their sleep and activity data beyond what is possible on the Oura app or website.


## Requirements

To use the Oura API you need a Personal Access Token (PAT), which can be created on the Oura website (once logged in):
https://cloud.ouraring.com/personal-access-tokens
- Press 'Create New Personal Access Token'
- Copy and save your PAT immediately, as you will not be able to view it again after leaving the page (don't worry, you can always create a new token!).

This token is used to access *your* personal data instead of someone else's.

## How It Works

Included are four functions for requesting sleep, activity, readiness and bedtime data. There are three more functions to create a full dataset, a shortened dataset, and to save any dataset as a CSV file.

You can get 6 different datasets and convert these to CSV files:
- `sleep.csv` for sleep data
- `activity.csv` for activity data
- `readiness.csv` for readiness data (i.e. some recovery indicators)
- `bedtime.csv` for bedtime data (ideal bedtimes)
- `full.csv` for a full, combined dataset with sleep, activity, readiness and bedtime data
- `short.csv` for a shortened version of the full dataset (e.g. most score contributors omitted)

To run:
- Paste your PAT on row 17 where indicated.
- On rows 21 and 21, type in the start and end dates of the period for which you want to request your data.
- Call the functions you want and the data sets are created.

Enjoy digging into your sleep data (there's tons)!
