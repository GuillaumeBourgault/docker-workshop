import sqlalchemy as sql
import click
import ingest_data

pg_user = "root"
pg_pass = "root"
pg_host = "localhost"
pg_port = "5432"
pg_db = "ny_taxi"


@click.command()
@click.option("--pg-host", default="localhost")
@click.option("--skip-ingestion", default=False)
def main(pg_host: str = "localhost", skip_ingestion: bool = False) -> None:
    if not skip_ingestion:
        ingest_data.main(pg_host)
    engine = sql.create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )
    Zones = sql.Table("zones", sql.MetaData(), autoload_with=engine)
    Trips = sql.Table("trips", sql.MetaData(), autoload_with=engine)
    question3(engine, Trips)
    question4(engine, Trips)
    question5(engine, Trips, Zones)
    question6(engine, Trips, Zones)


def question3(engine: sql.engine.base.Engine, Trips: sql.sql.schema.Table) -> None:
    # For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound),
    # how many trips had a trip_distance of less than or equal to 1 mile?
    stmt = sql.select(sql.func.count()).select_from(
        sql.select(Trips)
        .where(Trips.c.trip_distance <= 1.0)
        .where(Trips.c.lpep_pickup_datetime >= "2025-11-01")
        .where(Trips.c.lpep_pickup_datetime < "2025-12-01")
        .subquery()
    )
    with engine.connect() as conn:
        nb_trips = conn.execute(stmt).scalar_one()
    print(f"Question 3: {nb_trips} trips")


def question4(engine: sql.engine.base.Engine, Trips: sql.sql.schema.Table) -> None:
    # Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors)?
    with engine.connect() as conn:
        stmt1 = sql.select(sql.func.max(Trips.c.trip_distance)).where(
            Trips.c.trip_distance <= 100
        )
        longest_trip = conn.execute(stmt1).scalar_one()
        stmt2 = sql.select(Trips).where(Trips.c.trip_distance == longest_trip)
        rows = conn.execute(stmt2).all()
        assert len(rows) == 1
    print("Question 4:", rows[0]._mapping["lpep_pickup_datetime"])


def question5(
    engine: sql.engine.base.Engine,
    Trips: sql.sql.schema.Table,
    Zones: sql.sql.schema.Table,
) -> None:
    # Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?
    with engine.connect() as conn:
        stmt1 = (
            sql.select(
                Zones.c["Zone"],
                sql.func.sum(Trips.c["total_amount"]).label("revenue"),
            )
            .select_from(Trips)
            .join(Zones, Trips.c["PULocationID"] == Zones.c["LocationID"])
            .group_by(Zones.c["Zone"])
            .order_by(sql.desc("revenue"))
            .limit(1)
        )
        rows = conn.execute(stmt1).all()
        assert len(rows) == 1
    print("Question 5:", rows[0][0])


def question6(
    engine: sql.engine.base.Engine,
    Trips: sql.sql.schema.Table,
    Zones: sql.sql.schema.Table,
) -> None:
    # For the passengers picked up in the zone named "East Harlem North" in November 2025,
    # which was the drop off zone that had the largest tip?
    PUZones = Zones.alias("pu_zones")
    DOZones = Zones.alias("do_zones")
    with engine.connect() as conn:
        stmt1 = (
            sql.select(
                PUZones.c["Zone"].label("pickup_zone"),
                DOZones.c["Zone"].label("dropoff_zone"),
                Trips.c["tip_amount"],
            )
            .select_from(Trips)
            .join(PUZones, Trips.c["PULocationID"] == PUZones.c["LocationID"])
            .join(DOZones, Trips.c["DOLocationID"] == DOZones.c["LocationID"])
            .where(PUZones.c["Zone"] == "East Harlem North")
            .order_by(sql.desc("tip_amount"))
            .limit(1)
        )
        rows = conn.execute(stmt1).all()
        assert len(rows) == 1
    print("Question 6:", rows[0][1])


if __name__ == "__main__":
    main()
