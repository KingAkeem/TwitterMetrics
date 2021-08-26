# TwitterMetrics

This project allows users to analyze Twitter OSINT data and build reports using that data in various formats.

## Features

#### Search Tweets - you can seach a users tweets using various kinds of filters to view the information that is most relevant to you. There are currently 3 filters: tweet, time and location. 
- `keyword` filter returns tweets that contain the given text (e.g. `keyword: word_to_search`)
- `since` filter returns tweets that have occurred since a certain time period (e.g. `since:2021-11-14`, only `YYYY-mm-dd` date format is accepted)
- `until` filter returns tweets that have occurred until a certain time period (e.g. `until:2021-11-14`, only `YYYY-mm-dd` date format is accepted)
- `location` filter returns tweets that were made within a certain location (e.g. `location:56/102`, `lat/lon` respectively)
These filters can be used individually, separated by commas (e.g. `keyword:word_to_search,location:56/102`) or not used at all (in which case no data will be filtered and all tweets within the limit will be returned). Tweets can only be searched in increments of `20`.

#### Search User - you can search for a given user's profile and retrieve profile specific information.


## File Types Supported
- [X] CSV
- [X] JSON
- [ ] XLSX
- [ ] PDF
- [ ] ODF


## Setup & Installation
The core technologies used here are Python3, Flask, JavaScript, HTML/CSS, REST.

To start the app, 

1. you must have [`Flask`](https://flask.palletsprojects.com/en/2.0.x/installation/) installed.
2. Go to the root directory of this repository and run `flask run` in the terminal. 
