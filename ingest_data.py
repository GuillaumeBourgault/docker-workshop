#!/usr/bin/env python
# coding: utf-8
import sqlalchemy as sql
import sqlalchemy.orm
import pandas as pd
import click

pg_user = "root"
pg_pass = "root"
pg_port = "5432"
pg_db = "ny_taxi"


def ingest_zones(engine: sql.engine.base.Engine) -> None:
    session = sql.orm.sessionmaker(bind=engine)
    Session = session()
    table_name = "zones"
    url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
    df = pd.read_csv(url)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")
    df.to_sql(name=table_name, con=engine, if_exists="append")
    table = sql.Table(table_name, sql.MetaData(), autoload_with=engine)
    nb_stored_rows = Session.query(table).count()
    assert nb_stored_rows == len(df)
    print(f"{nb_stored_rows} entries created in table {table}")


def ingest_data_green(
    engine,
) -> pd.DataFrame:
    table_name = "trips"
    url = (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
    )
    df = pd.read_parquet(url, engine="pyarrow")
    df.head(0).to_sql(name=table_name, con=engine, if_exists="replace")
    df.to_sql(name=table_name, con=engine, if_exists="append")
    table = sql.Table(table_name, sql.MetaData(), autoload_with=engine)
    session = sql.orm.sessionmaker(bind=engine)
    Session = session()
    nb_stored_rows = Session.query(table).count()
    assert nb_stored_rows == len(df)
    print(f"{nb_stored_rows} entries created in table {table}")


def main(pg_host):
    engine = sql.create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )
    ingest_zones(engine)
    ingest_data_green(engine)
