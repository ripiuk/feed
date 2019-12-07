# Feed


### Description

This project provides some data **Feeds** (food) for its clients.

Expose a dataset through a single generic HTTP API endpoint, which is capable of filtering, grouping and sorting.

Clients of this API are able to:
1. filter by time range (date_from / date_to is enough), channels, countries, operating systems
1. group by one or more columns: date, channel, country, operating system
1. sort by any column in ascending or descending order
1. see derived metric CPI (cost per install) which is calculated as cpi = spend / installs


### How to run locally

Install python, create virtual environment and install all the requirements:

    make setup

Install PostgreSQL:

    make install-psql

Create `feed/.env` configuration file with custom settings. Example of the `feed/.env` file:

    DEBUG=True
    SECRET_KEY=Some secret key here
    DATABASE_URL=psql://user_name:user_password@localhost:5432/feed

Run the project:

    make run

It will open your browser on http://127.0.0.1:8000/usage_info


### How to run tests

Run the tests:

    make test


### Usage Examples

1. Show the number of impressions and clicks that occurred before the 1st of June 2017, 
broken down by channel and country, sorted by clicks in descending order

        $ curl "http://127.0.0.1:8000/usage_info?date_to=2017-06-01&group_by=channel,country&sort_by=-clicks" | python3.7 -m json.tool
        {
            "count": 25,
            "next": null,
            "previous": null,
            "results": [
                {
                    "date": null,
                    "channel": "adcolony",
                    "country": "US",
                    "os": null,
                    "impressions": 532608,
                    "clicks": 13089,
                    "installs": 2417,
                    "spend": 3926.7,
                    "revenue": 6485.94
                },
                {
                    "date": null,
                    "channel": "apple_search_ads",
                    "country": "US",
                    "os": null,
                    "impressions": 369993,
                    "clicks": 11457,
                    "installs": 2235,
                    "spend": 4470.0,
                    "revenue": 7432.99
                },
                {
                    "date": null,
                    "channel": "vungle",
                    "country": "GB",
                    "os": null,
                    "impressions": 266470,
                    "clicks": 9430,
                    "installs": 1809,
                    "spend": 3618.0,
                    "revenue": 5275.2
                },
                {
                    "date": null,
                    "channel": "vungle",
                    "country": "US",
                    "os": null,
                    "impressions": 266976,
                    "clicks": 7937,
                    "installs": 1676,
                    "spend": 3352.0,
                    "revenue": 4930.42
                },
                ...

1. Show the number of installs that occurred in May of 2017 on iOS, 
broken down by date, sorted by date in ascending order.

        $ curl "http://127.0.0.1:8000/usage_info?date_from=2017-05-01&date_to=2017-05-31&os=ios&group_by=date&sort_by=date" | python3.7 -m json.tool
        {
        "count": 15,
        "next": null,
        "previous": null,
        "results": [
            {
                "date": "2017-05-17",
                "channel": null,
                "country": null,
                "os": null,
                "impressions": 126743,
                "clicks": 3903,
                "installs": 755,
                "spend": 1479.72,
                "revenue": 1835.75
            },
            {
                "date": "2017-05-18",
                "channel": null,
                "country": null,
                "os": null,
                "impressions": 127028,
                "clicks": 3803,
                "installs": 765,
                "spend": 45142.29,
                "revenue": 1804.16
            },
            {
                "date": "2017-05-19",
                "channel": null,
                "country": null,
                "os": null,
                "impressions": 126354,
                "clicks": 3966,
                "installs": 745,
                "spend": 1516.75,
                "revenue": 2287.7
            },
            {
                "date": "2017-05-20",
                "channel": null,
                "country": null,
                "os": null,
                "impressions": 156588,
                "clicks": 4640,
                "installs": 816,
                "spend": 1685.48,
                "revenue": 2350.42
            },
            ...

1. Show revenue, earned on June 1, 2017 in US, broken down by operating system 
and sorted by revenue in descending order.

        $ curl "http://127.0.0.1:8000/usage_info?date_from=2017-06-01&date_to=2017-06-01&countries=US&group_by=os&sort_by=-revenue" | python3.7 -m json.tool
        {
            "count": 2,
            "next": null,
            "previous": null,
            "results": [
                {
                    "date": null,
                    "channel": null,
                    "country": null,
                    "os": "android",
                    "impressions": 61050,
                    "clicks": 1675,
                    "installs": 334,
                    "spend": 662.96,
                    "revenue": 1205.21
                },
                {
                    "date": null,
                    "channel": null,
                    "country": null,
                    "os": "ios",
                    "impressions": 55676,
                    "clicks": 1737,
                    "installs": 306,
                    "spend": 630.76,
                    "revenue": 398.87
                }
            ]
        }

1. Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order.

        $ curl "http://127.0.0.1:8000/usage_info?cpi=1&countries=CA&group_by=channel&sort_by=-cpi" | python3.7 -m json.tool
        {
            "count": 4,
            "next": null,
            "previous": null,
            "results": [
                {
                    "date": null,
                    "channel": "facebook",
                    "country": null,
                    "os": null,
                    "impressions": 99126,
                    "clicks": 2910,
                    "installs": 561,
                    "spend": 1164.0,
                    "revenue": 1928.0,
                    "cpi": 2.07486631016043
                },
                {
                    "date": null,
                    "channel": "chartboost",
                    "country": null,
                    "os": null,
                    "impressions": 98880,
                    "clicks": 2978,
                    "installs": 637,
                    "spend": 1274.0,
                    "revenue": 1760.8,
                    "cpi": 2.0
                },
                {
                    "date": null,
                    "channel": "unityads",
                    "country": null,
                    "os": null,
                    "impressions": 198767,
                    "clicks": 6822,
                    "installs": 1321,
                    "spend": 2642.0,
                    "revenue": 3579.6,
                    "cpi": 2.0
                },
                {
                    "date": null,
                    "channel": "google",
                    "country": null,
                    "os": null,
                    "impressions": 99318,
                    "clicks": 2910,
                    "installs": 574,
                    "spend": 999.9,
                    "revenue": 1270.0,
                    "cpi": 1.74198606271777
                }
            ]
        }
