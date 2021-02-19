# Oura-Ring-API-Tools

This script provides some useful tools to help working with the Oura Sleep Ring API.

The API documentation on Oura's website provides very little guidance and some sections are not even documented, which is why I created this project. I hope this is helpful for anyone who wants to download and analyse their Oura sleep data beyond what is possible on the official app or the website.


## Requirements

To be able to use the Oura API, you need to have an Oura account. Assuming that you are an Oura user, you will already have the account set up.

In addition, you need a Personal Access Token (PAT), which can be created on the Oura website (once logged in):
https://cloud.ouraring.com/personal-access-tokens
- Press 'Create New Personal Access Token'
- Copy and save your PAT immediately, as you will not be able to view it again after leaving the page (don't worry, you can always create a new token!).

This token is used to access *your* personal data instead of someone else's.

## How It Works

`get-ring-data.py` is a script used to download all the user data the Oura API has to offer (there's tons!).

It returns 6 CSV files:
- `sleep.csv` for all sleep data
- `activity.csv` for all activity data
- `readiness.csv` for readiness data (i.e. some recovery indicators and lagged values)
- `bedtime.csv` for bedtime data (ideal bedtimes)
- `combined.csv` for a combined dataset with sleep, activity, and readiness data (bedtime data left out)
- `short.csv` for a shortened version of the combined dataset (e.g. most score contributors omitted)

To run:
- Paste your PAT on row 19 where indicated.
- On rows 25 and 26, type in the start and end dates of the period for which you want the data.
- Run the script and the CSV files are created.

Enjoy digging into your sleep data!
