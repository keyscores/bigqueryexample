import argparse
import csv
import httplib2
import json
import os
import pprint
import re
import time

from cStringIO import StringIO

import xlrd
import cloudstorage as gcs
import webapp2

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.appengine import AppAssertionCredentials
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client import tools
from oauth2client.tools import run_flow
from google.appengine.api import app_identity

from util import is_content_type_excel, write_gcs_file

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
GCE_SCOPE = 'https://www.googleapis.com/auth/compute'
FLOW = flow_from_clientsecrets(CLIENT_SECRETS, scope=GCE_SCOPE)


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
                    first_row = sh.row_values(0)
                    for idx, col in enumerate(first_row):
                        clean_col = col.replace(" ", "_")
                        clean_col = re.sub('[()]', '', clean_col)
                        first_row[idx] = clean_col
                    c.writerow(first_row)
                    for r in range(1, sh.nrows):
                        c.writerow(sh.row_values(r))
                    filename = str(filename) + '_' + str(sn)
                    gcs_filename = os.path.join(bucket, filename + '.csv')
                    csv_file.seek(0)
                    data = csv_file.read()
                    write_gcs_file(
                        gcs_filename, data, 'text/csv'
                    )


SCOPE = 'https://www.googleapis.com/auth/bigquery'
PROJECT_NUMBER = '266479093208'


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
        # OAuth based work flow
        # Create a storage file to save the credentials
        # parser = argparse.ArgumentParser(
        #     description=__doc__,
        #     formatter_class=argparse.RawDescriptionHelpFormatter,
        #     parents=[tools.argparser]
        # )
        # flags = parser.parse_args({})
        # storage = Storage('bigquery-credentials.dat')
        # credentials = storage.get()
        # if credentials is None or credentials.invalid:
        #     credentials = run_flow(FLOW, storage, flags)

        # big query based auth flow
        credentials = AppAssertionCredentials(scope=SCOPE)

        # Create a httplib2.Http object to handle HTTP requests and authorize it
        # with our valid credentials
        http = credentials.authorize(httplib2.Http())

        self.response.content_type = 'application/json'

        service = build('bigquery', 'v2', http=http)
        try:
            job_collection = service.jobs()
            job_data = json.loads(self.request.body)
            project_id = self.request.headers['X-Keyscores-Project-Id']
            insert_response = job_collection.insert(
                projectId=project_id, body=job_data
            ).execute()
            # Ping for status until the loading job is done, with a short pause between calls.
            while True:
                job = job_collection.get(
                    projectId=project_id,
                    jobId=insert_response['jobReference']['jobId']
                ).execute()
                if 'DONE' == job['status']['state']:
                    print('DONE Loading!')
                    data = {
                        'status': 'success'
                    }
                    self.response.out.write(json.dumps(data))
                    return

                print 'Waiting for loading to complete...'
                time.sleep(15)

            if 'errorResult' in job['status']:
                logging.info('Error loading table: ', pprint.pprint(job))
                data = {
                    'status': 'error',
                    'job': pprint.pprint(job),
                    'insert_response': insert_response
                }
                self.response.out.write(json.dumps(data))
                return
        except HttpError as err:
            logging.info('Error loading data: ', pprint.pprint(err))
            data = {
                'status': 'error',
                'job': pprint.pprint(err.resp)
            }
            self.response.out.write(json.dumps(data))
            return

import logging
from google.appengine.api import urlfetch


def create_short_url(long_url):
    scope = "https://www.googleapis.com/auth/urlshortener"
    authorization_token, _ = app_identity.get_access_token(scope)
    logging.info("Using token %s to represent identity %s",
                 authorization_token, app_identity.get_service_account_name())
    payload = json.dumps({"longUrl": long_url})
    response = urlfetch.fetch(
            "https://www.googleapis.com/urlshortener/v1/url?pp=1",
            method=urlfetch.POST,
            payload=payload,
            headers = {"Content-Type": "application/json",
                       "Authorization": "OAuth " + authorization_token})
    if response.status_code == 200:
        result = json.loads(response.content)
        return result["id"]
    raise Exception("Call failed. Status code %s. Body %s",
                    response.status_code, response.content)


class URLShortnerHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(create_short_url(self.request.GET['long_url']))
        return


application = webapp2.WSGIApplication([
    ('/upload', ImportDataHandler),
    ('/load_data', BigQueryLoadDataHandler),
    ('/shorten_url', URLShortnerHandler)
], debug=True)
