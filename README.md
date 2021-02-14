# Oura-Ring-API-Tools

This script provides some useful tools that help working with the Oura Sleep Ring API.

The API documentation on Oura's website provides very little guidance, which is why I created this project. I hope this is helpful for anyone who wants to download and analyse their Oura sleep data beyond what is possible on the official app.


## Requirements

To be able to use the Oura API, you need to have an Oura account. Assuming that you use the ring, this step should already be done.

In addition, you need a Personal Access Token (PAT), which can be created on Oura website (once logged in):
https://cloud.ouraring.com/personal-access-tokens
- Press 'Create New Personal Access Token'
- Copy and save your PAT immediately, as you will not be able to view it again after leaving the page (don't worry, you can always create a new token!).

## How It Works

This project includes two parts:

### 1. `get-ring-data.py` is a script used to download all the user data the Oura API has to offer (there's tons!).

It returns 6 CSV files:
- `sleep.csv` for all sleep data
- `activity.csv` for all activity data
- `readiness.csv` for readiness data (i.e. some recovery indicators and lagged values)
- `bedtime.csv` for bedtime data (ideal bedtimes only)
- `combined.csv` for a combined dataset with sleep, activity, and readiness data (bedtime data left out)
- `trimmed.csv` for a trimmed version of the full combined dataset (for example, most score contributors omitted)

To run `get-ring-data.py`:
- Paste your PAT on row 22 where indicated.
- On row 28 and 29, type in the start and end dates of the period for which you want the data.
- Run the script and the beforementioned CSV files are created.


### 2. `visualize.py` is a script for plotting all this data. These include:
- Sleep, activity, and readiness trends
- 

