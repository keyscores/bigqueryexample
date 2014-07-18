import csv
import os

from cStringIO import StringIO

import xlrd
import cloudstorage as gcs
import webapp2

from google.appengine.api import app_identity

from util import is_content_type_excel, write_gcs_file


class ImportDataHandler(webapp2.RequestHandler):
    def post(self):
        bucket_name = self.request.headers.get(
            'X-Keyscores-Bucket-Name',
            app_identity.get_default_gcs_bucket_name()
        )
        bucket = '/' + bucket_name
        filename = self.request.headers['X-Keyscores-Filename']
        file_data = self.request.body
        content_type = self.request.headers['Content-Type'].split(';')[0]
        if is_content_type_excel(content_type):
            # Convert each sheet in the excel file into a csv file
            # and uploads the the csv file's data onto cloud storage
            # instead of the original excel file
            with xlrd.open_workbook(file_contents=self.request.body_file.read()) as wb:
                for sn in wb.sheet_names():
                    sh = wb.sheet_by_name(sn)
                    csv_file = StringIO()
                    c = csv.writer(csv_file)
                    for r in range(sh.nrows):
                        c.writerow(sh.row_values(r))
                    filename = str(filename) + '_' + str(sn)
                    gcs_filename = os.path.join(bucket, filename + '.csv')
                    csv_file.seek(0)
                    data = csv_file.read()
                    write_gcs_file(
                        gcs_filename, data, 'text/csv'
                    )


class BigQueryLoadDataHandler(webapp2.RequestHandler):
    def post(self):
        """
        Accept a serialized JSON POST request to create a data loading
        job to load a cloud storage file into a table on big query.

        For example, the JSON object could look like:
        {
            'projectId': projectId,
            'configuration': {
                'load': {
                    'sourceUrls': [gs://bucket_name/csv_filename],
                    'schema': {
                        'fields': [
                            {
                                'name': 'CLV',
                                'type': 'FLOAT'
                            },
                            ...
                        ]
                    },
                    'destinationTable': {
                        'projectId': %(projectId)s,
                        'datasetId': %(datasetId)s,
                        'tableId': %(targetTableId)s
                    }
                }
            }
        }
        """


application = webapp2.WSGIApplication([
    ('/upload', ImportDataHandler)
], debug=True)
