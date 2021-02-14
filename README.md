# Oura-Ring-API-Tools

This script provides some useful tools to work with the Oura Sleep Ring API.

Background: I'm a happy owner of Oura Ring and wanted to analyse my sleep data beyond what the app allows. It seemed difficult to find these basic tools online (Oura is still up-and-coming), so I decided to create this project. I hope this is helpful for anyone who wants to dive deeper into their sleep data.

### How It Works

1. `get-ring-data.py` is the script used to download all the data a user has.

It returns 5 CSV files:
- `sleep.csv` for all sleep data
- `activity.csv` for all activity data
- `readiness.csv` for readiness data (i.e. some recovery indicators and lagged values)
- `combined.csv` for all of these three datasets combined
- `modified.csv` for a trimmed version the combined data

2. `visualize.py` is a script for plotting the data returned by `get-ring-data.py`. These include:
- 
