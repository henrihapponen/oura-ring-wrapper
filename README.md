# oura-ring-rrapper

This script provides some useful, lightweight functions that make it easier to work with the Oura Ring API.

The API documentation on Oura's website provides very little guidance, with some sections lacking documentation altogether, which is why I created this project. I hope this is helpful for anyone who wants to download and analyse their sleep and activity data beyond what is possible on the Oura app or website.


## Requirements

To use the Oura API you need a Personal Access Token (PAT), which can be created on the Oura website (once logged in):
https://cloud.ouraring.com/personal-access-tokens
- Press "Create New Personal Access Token"
- Copy and save your PAT immediately, as you will not be able to view it again after leaving the page (don't worry, you can always create a new token!).

This token is used to access *your* personal data instead of someone else's.

Other requirements are in the `requirements.txt` file. Use `pip install -r requirements.txt` or `python -m pip install -r requirements.txt` to install.

## How It Works

Included are four functions for requesting sleep, activity, readiness and bedtime data. There are two more functions to create a full dataset and a shortened dataset.

You can get 6 different datasets using these functions:
- `get_sleep_data` for all sleep data
- `get_activity_data` for all activity data
- `get_readiness_data` for readiness data (like recovery indicators)
- `get_bedtime_data` for bedtime data (ideal bedtimes)
- `merge_all_to_full` for a full, combined dataset with sleep, activity, readiness and bedtime data
- `get_short_dataset` for a shortened version of the full dataset (e.g. most score contributors omitted)

Before you run:
- Replace your PAT where indicated.
- Where indicated, replace the start and end dates of the period for which you want to request your data.
- Call the functions you want and the data sets are created.

Enjoy digging into your sleep data!
