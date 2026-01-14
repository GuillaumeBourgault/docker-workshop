#!/usr/bin/env python
# coding: utf-8
import sqlalchemy as sql
import sqlalchemy.orm
import pandas as pd
from tqdm.auto import tqdm


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
    "congestion_surcharge": "float64",
}

parse_dates = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]


def ingest_zones(engine: sql.engine.base.Engine) -> None:
    session = sql.orm.sessionmaker(bind=engine)
    Session = session()
    table_name = "zones"
    url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
    df = pd.read_csv(url)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")
    df.to_sql(name=table_name, con=engine, if_exists="append")
    zones = sql.Table(table_name, sql.MetaData(), autoload_with=engine)
    nb_stored_rows = Session.query(zones).count()
    assert nb_stored_rows == len(df)
    print(f"{nb_stored_rows} taxi zones stored")


def ingest_data_green(
    engine,
) -> pd.DataFrame:
    url = (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
    )
    chunksize = 100000
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )

    first_chunk = next(df_iter)

    first_chunk.head(0).to_sql(name=target_table, con=engine, if_exists="replace")

    print(f"Table {target_table} created")

    first_chunk.to_sql(name=target_table, con=engine, if_exists="append")

    print(f"Inserted first chunk: {len(first_chunk)}")

    for df_chunk in tqdm(df_iter):
        df_chunk.to_sql(name=target_table, con=engine, if_exists="append")
        print(f"Inserted chunk: {len(df_chunk)}")

    print(f"done ingesting to {target_table}")


def main(
    pg_user="root",
    pg_pass="root",
    pg_host="localhost",
    pg_port="5432",
    pg_db="ny_taxi",
):
    engine = sql.create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )
    ingest_zones(engine)


if __name__ == "__main__":
    main()
