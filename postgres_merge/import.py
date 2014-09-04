import argparse

import xlrd
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from postgres_merge.models import Base, RawData


def import_data(args):
    engine = create_engine(args.postgres)
    Base.metadata.bind = engine
    Base.metadata.create_all(bind=engine)
    DBSession = sessionmaker()
    DBSession.bind = engine

    s = DBSession()
    csv_filenames = args.filenames
    connector_version = args.connector_version
    connector_name = args.connector
    for csv_filename in csv_filenames:
        wb = xlrd.open_workbook(csv_filename)
        sheet = wb.sheet_by_index(0)
        sheet_name = sheet.name
        columns = sheet.row(0)
        for row_index in range(1, sheet.nrows):
            values = sheet.row(row_index)
            data = dict()
            for index, key in enumerate(columns):
                data[key.value] = str(values[index].value)
            raw_data = RawData(
                data=data, connector=connector_name,
                version=connector_version,
                sheet_name=sheet_name, file_name=csv_filename
            )
            s.add(raw_data)
            s.flush()
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
                        required=True, type=str,
                        help="""
                        version of the connector
                        """)
    args = parser.parse_args()
    import_data(args)
