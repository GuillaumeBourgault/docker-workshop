import sqlalchemy as sql
import sqlalchemy.orm as orm
from importlib.metadata import version
import click

pg_user = "root"
pg_pass = "root"
pg_host = "localhost"
pg_port = "5432"
pg_db = "ny_taxi"


@click.command()
@click.option("--pg-host", default="localhost")
def main(pg_host: str = "localhost") -> None:
    engine = sql.create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )
    Zones = sql.Table("zones", sql.MetaData(), autoload_with=engine)
    Trips = sql.Table("trips", sql.MetaData(), autoload_with=engine)
    session = sql.orm.sessionmaker(bind=engine)
    Session = session()
    question3(Session, Trips)
    question4(Session)
    question5(Session)
    question6(Session)
    question7(Session)


def question3(Session: orm.session.Session, Trips: sql.sql.schema.Table) -> None:
    print(
        """
    Question 3
    For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), 
    how many trips had a trip_distance of less than or equal to 1 mile?
    """
    )
    nb_trips = (
        Session.query(Trips)
        .where(Trips.c.trip_distance <= 1.0)
        .where(Trips.c.lpep_pickup_datetime >= "2025-11-01")
        .where(Trips.c.lpep_pickup_datetime < "2025-12-01")
        .count()
    )
    print("Answer:", nb_trips, "trips")


def question4(Session: orm.session.Session) -> None:
    return


def question5(Session: orm.session.Session) -> None:
    return


def question6(Session: orm.session.Session) -> None:
    return


def question7(Session: orm.session.Session) -> None:
    return


if __name__ == "__main__":
    main()
