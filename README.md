# Oura-Ring-API-Tools

This script provides some useful tools to work with the Oura Sleep Ring API.

I couldn't find anything like this online so I decided to create this project. I hope this is helpful for anyone who wants to dive deeper into their Oura sleep data.

## How It Works

This project includes three parts:

### 1. `get-ring-data.py` is a script used to download all the data a Oura user has.

It returns 6 CSV files:
- `sleep.csv` for all sleep data
- `activity.csv` for all activity data
- `readiness.csv` for readiness data (i.e. some recovery indicators and lagged values for example)
- `bedtime.csv` for bedtime data (only ideal bedtimes)
- `combined.csv` for combined dataset with sleep, activity, and readiness data (ideal bedtimes left out)
- `trimmed.csv` for a trimmed version the full combined dataset (e.g. most score contributors omitted)

For this part, you need a Personal Access Token (PAT), which can be created on Oura website (once logged in first:
https://cloud.ouraring.com/personal-access-tokens
- Press 'Create New Personal Access Token'
- Copy and save this immediately, as you will not be able to see it again once you leave the page (but don't worry, you can always create a new token!).

Paste your PAT on row 22 of `get-ring-data.py`

On row 28 and 29, type in the start and end dates of the period for which you want the data

Run the script and the above mentioned CSV files are created.


### 2. `visualize.py` is a script for plotting all this data. These include:
- Sleep, activity, and readiness trends
- 


### 3. `insights.py` is an attempt to get new insight additional to what Oura provides on their app
- 

