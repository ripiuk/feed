import csv
from pathlib import Path
from contextlib import closing

import environ
import psycopg2


env = environ.Env()
environ.Env.read_env(str(Path(__file__).parents[2] / 'feed' / '.env'))
conn_params = env.db()

FILE = 'usage_info/samples/dataset.csv'

INSERT_QUERY = """
    INSERT INTO usage_info_usageinfo(date, channel, country, os, impressions,
        clicks, installs, spend, revenue)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

with closing(psycopg2.connect(
        host=conn_params['HOST'],
        dbname=conn_params['NAME'],
        user=conn_params['USER'],
        password=conn_params['PASSWORD'])) as db_conn:
    with db_conn.cursor() as curr:
        print('Insert begins ...')
        counter = 0

        with open(FILE, 'rt') as csvf:
            reader = csv.reader(csvf)
            next(reader)  # skip header

            for record in reader:
                curr.execute(INSERT_QUERY, record)
                counter += 1
                if counter % 100 == 0:
                    db_conn.commit()
            db_conn.commit()

print('Done. Inserted', counter, 'records')
