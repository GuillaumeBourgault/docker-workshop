#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from tqdm.auto import tqdm
from datetime import datetime
import click

url_prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

def is_data_present(engine,target_table,
        year:int, 
        month:int,)->bool:
    start = datetime(year, month, 1)
    end = datetime(year, month+1,1)
    query = text(f'''
        SELECT *
        FROM {target_table}
        WHERE tpep_pickup_datetime >= :start
        AND tpep_pickup_datetime < :end
        LIMIT 1
        ''', 
    )
    with engine.connect() as conn:
        rows = conn.execute(query, {"start": start, "end": end}).fetchall()
        print('rows')
        print(rows)
    return True

def ingest_data(
        year:int, 
        month:int,
        engine,
        target_table: str,
        chunksize: int = 100000,
        overwrite:bool=False
) -> pd.DataFrame:
    if overwrite or not is_data_present(engine, target_table, year, month):
        url = f'{url_prefix}/yellow_tripdata_{year:04d}-{month:02d}.csv.gz'
        print(url)
        # before ingesting, check if there.  
        df_iter = pd.read_csv(
            url,
            dtype=dtype,
            parse_dates=parse_dates,
            iterator=True,
            chunksize=chunksize
        )

        first_chunk = next(df_iter)

        first_chunk.head(0).to_sql(
            name=target_table,
            con=engine,
            if_exists="replace"
        )

        print(f"Table {target_table} created")

        first_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append"
        )

        print(f"Inserted first chunk: {len(first_chunk)}")

        for df_chunk in tqdm(df_iter):
            df_chunk.to_sql(
                name=target_table,
                con=engine,
                if_exists="append"
            )
            print(f"Inserted chunk: {len(df_chunk)}")

        print(f'done ingesting to {target_table}')

def main(
        year=2025, 
        month=11, 
        pg_user='root', 
        pg_pass='root', 
        pg_host='pgdatabase', 
        pg_port='5432', 
        pg_db='ny_taxi', 
        chunksize=100000, 
        target_table='yello_taxi_data', 
        overwrite=True
    ):
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    ingest_data(
        year, 
        month,
        engine=engine,
        target_table=target_table,
        chunksize=chunksize,
        overwrite=overwrite
    )

if __name__ == '__main__':
    main()