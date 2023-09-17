# oura-ring-wrapper

Simple, lightweight functions that make it easy to work with the Oura Ring API!

I hope this is useful for anyone who wants to download and analyse their sleep and activity data beyond what's possible on the Oura app or website.

The functions in this script are based on the API v2 documentation available here: https://cloud.ouraring.com/v2/docs

## Requirements

To use the Oura API you need a Personal Access Token (PAT), which can be created on the Oura website (once logged in):
https://cloud.ouraring.com/personal-access-tokens
- Press "Create New Personal Access Token"
- Copy and save your PAT immediately, as you will not be able to view it again after leaving the page (but you can always create a new token!).

This token is used to access *your* personal data instead of someone else's.

Project dependencies are listed in the `pyrpoject.toml` file. Use `pip install .` to install them.

## How It Works

This script includes three functions to request data from the Oura API:
- `request_user_info` for requesting basic user information
- `request_data` for requesting data sets
- `request_flat_data` for requesting data sets with the **contributors** field flattened out into separate columns

These are the data sets you can request:
- `sleep`
- `daily_sleep`
- `daily_activity`
- `daily_readiness`
- `sleep_time`
- `tag`
- `workout`
- `session`
- `daily_spo2`
- `heartrate`
- `rest_mode_period`

Flat versions (using the `request_flat_data` function) are available for the following data sets:
- `daily_sleep`
- `daily_activity`
- `daily_readiness`

Before you run:
- Replace your PAT where indicated.
- Where indicated, replace the start and end dates of the period for which you want to request your data.
- Specify the data sets you want and the download can begin.

Enjoy digging into your sleep data!
