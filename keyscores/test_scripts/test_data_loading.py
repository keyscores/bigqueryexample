import json
import os
import unittest

import requests

testing_project_id = 'kinetic-physics-644'
loading_job_data = {
    'Country_and_Region.xlsx_Sheet1.csv': {
        'projectId': testing_project_id,
        'configuration': {
            'load': {
                'sourceUris': ['gs://keyscores_test/Country_and_Region.xlsx_Sheet1.csv'],
                'schema': {
                    'fields': [
                        {
                            'name': 'Country Code',
                            'type': 'STRING'
                        },
                        {
                            'name': 'Region',
                            'type': 'STRING'
                        }
                    ]
                },
                'destinationTable': {
                    'projectId': testing_project_id,
                    'datasetId': 'Country_and_Region',
                    'tableId': 'Country_and_Region_Sheet1_Table'
                }
            }
        }
    }
}


class CountryAndRegionLoadingTestCase(unittest.TestCase):
    def test_country_and_region_data_loading(self):
        """
        POST a JSON document towards the endpoint /load_data
        should load the country and region data from cloud
        storage into big query.

        In this test case, we perform the following operation:
        1. POST the JSON document loading_job_data to the endpoint
        /load_data
        2. GET a JSON document describing the job status from
        the endpoint /get_job/{job_id} and verify that the data
        loading job has finished
        """
        # POST the JSON document loading_job_data to the endpoint
        # /load_data
        server_url = os.environ['SERVER_URL']
        url = os.path.join(server_url, 'load_data')
        resp = requests.post(
            url, data=json.dumps(loading_job_data),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'text/plain',
                'X-Keyscores-Project-Id': testing_project_id
            }
        )
        self.assertEqual(resp.status_code, 200)
