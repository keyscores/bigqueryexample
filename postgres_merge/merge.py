import argparse
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from postgres_merge.models import Base, RawData, MergedData


def merge_data(args):
    engine = create_engine(args.postgres)
    Base.metadata.bind = engine
    Base.metadata.create_all(bind=engine)
    DBSession = sessionmaker()
    DBSession.bind = engine

    s = DBSession()
    ctes = []
    raw_data = RawData.__table__
    for filename in args.filenames:
        cte = sa.select([raw_data.c.data]).where(
            sa.and_(
                raw_data.c.file_name == filename,
                raw_data.c.connector == args.connector,
                raw_data.c.version == args.connector_version
            )
        ).cte(filename)
        ctes.append(cte)
    selected_cols = ctes[0].c.data
    for cte in ctes[1:]:
        selected_cols = selected_cols + cte.c.data
    select_from = ctes[0].join(
        ctes[1], ctes[0].c.data['Country_Code'] == ctes[1].c.data['Country_Code']
    )
    merge_stmt = sa.select([selected_cols]).select_from(select_from)
    rs = s.execute(merge_stmt)
    for rst in rs:
        merged_data = MergedData(
            data=rst[0], connector=args.connector,
            version=args.connector_version
        )
        s.add(merged_data)
    s.commit()
    s.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filenames', nargs='+',
                        required=True, type=str,
                        help="""
                        a list of CSV files to import
                        """)
    parser.add_argument('--postgres',
                        required=True, type=str,
                        help="""
                        a PostgreSQL connection string
                        """)
    parser.add_argument('--connector',
                        required=True, type=str,
                        help="""
                        name of the connector
                        """)
    parser.add_argument('--connector-version',
                        required=True, type=int,
                        help="""
                        version of the connector
                        """)
    args = parser.parse_args()
    merge_data(args)