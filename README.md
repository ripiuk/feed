# Feed


### Description

This project provides some data **Feeds** (food) for its clients.

Expose a dataset through a single generic HTTP API endpoint, which is capable of filtering, grouping and sorting.

Client of this API are able to:
1. filter by time range (date_from / date_to is enough), channels, countries, operating systems
1. group by one or more columns: date, channel, country, operating system
1. sort by any column in ascending or descending order
1. see derived metric CPI (cost per install) which is calculated as cpi = spend / installs


### How to run locally

Install python, create virtual environment and install all the requirements:

    make setup

Create `feed/.env` configuration file with custom settings. Example of the `feed/.env` file:

    DEBUG=True
    SECRET_KEY=Some secret key here
    DATABASE_URL=psql://user_name:user_password@localhost:5432/feed

Run the project:

    make run

It will open your browser on http://127.0.0.1:8000/