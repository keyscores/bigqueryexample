import json
import os
import time
import unittest

import requests

testing_project_id = 'kinetic-physics-644'
testing_dataset_id = 'Raw_Data'
country_and_region_configuration = {
    'projectId': testing_project_id,
    'configuration': {
        'load': {
            'sourceUris': ['gs://keyscores_test/Country_and_Region.xlsx_Sheet1.csv'],
            'schema': {
                'fields': [
                    {
                        'name': 'Country_Code',
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
                'datasetId': testing_dataset_id,
                'tableId': 'Country_and_Region_Sheet1_Table'
            },
            'skipLeadingRows': 1
        }
    }
}
currency_configuration = {
    'projectId': testing_project_id,
    'configuration': {
        'load': {
            'sourceUris': ['gs://keyscores_test/Currency.xlsx_Sheet1.csv'],
            'schema': {
                'fields': [
                    {
                        'name': 'Exchange_Rate',
                        'type': 'STRING'
                    },
                    {
                        'name': 'Month',
                        'type': 'STRING'
                    },
                    {
                        'name': 'Customer_Currency',
                        'type': 'STRING'
                    }
                ]
            },
            'destinationTable': {
                'projectId': testing_project_id,
                'datasetId': testing_dataset_id,
                'tableId': 'Currency_Sheet1_Table'
            },
            'skipLeadingRows': 1
        }
    }
}
sales_configuration = {
    'projectId': testing_project_id,
    'configuration': {
        'load': {
            'sourceUris': ['gs://keyscores_test/Sales.xlsx_Sheet1.csv'],
            'schema': {
                'fields': [
                    {
                        'name': 'Vendor_Identifier',
                        'type': 'STRING'
                    },
                    {
                        'name': 'Product_Type_Identifier',
                        'type': 'STRING'
                    },
                    {
                        'name': 'Units',
                        'type': 'FLOAT'
                    },
                    {
                        'name': 'Royalty_Price',
                        'type': 'FLOAT'
                    },
                    {
                        'name': 'Download_Date_PST',
                        'type': 'STRING'
                    },
                    {
                        'name': 'Customer_Currency',
                        'type': 'STRING'
                    },
                    {
                        'name': 'Country_Code',
                        'type': 'STRING'
                    }
                ]
            },
            'destinationTable': {
                'projectId': testing_project_id,
                'datasetId': testing_dataset_id,
                'tableId': 'Sales_Sheet1_Table'
            },
            'skipLeadingRows': 1
        }
    }
}
commission_and_tax_configuration = {
    'projectId': testing_project_id,
    'configuration': {
        'load': {
            'sourceUris': ['gs://keyscores_test/Comission_and_Tax.xlsx_Sheet1.csv'],
            'schema': {
                'fields': [
                    {
                        'name': 'Vendor_Identifier',
                        'type': 'STRING'
                    },
                    {
                        'name': 'Region',
                        'type': 'STRING'
                    },
                    {
                        'name': 'Rights_Holder',
                        'type': 'STRING'
                    },
                    {
                        'name': 'Comission',
                        'type': 'FLOAT'
                    },
                    {
                        'name': 'Tax',
                        'type': 'FLOAT'
                    }
                ]
            },
            'destinationTable': {
                'projectId': testing_project_id,
                'datasetId': testing_dataset_id,
                'tableId': 'Comission_and_Tax_Sheet1_Table'
            },
            'skipLeadingRows': 1
        }
    }
}

job_data = {
    'Country_and_Region': country_and_region_configuration,
    'Currency': currency_configuration,
    'Sales': sales_configuration,
    "Commission_and_Tax": commission_and_tax_configuration
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
        # POST the JSON document job_data to the endpoint
        # /load_data
        server_url = os.environ['SERVER_URL']
        url = os.path.join(server_url, 'load_data')
        for key, val in job_data.iteritems():
            print("Loading {0}".format(key))
            resp = requests.post(
                url, data=json.dumps(val),
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'text/plain',
                    'X-Keyscores-Project-Id': testing_project_id
                }
            )
            self.assertEqual(resp.status_code, 200)
            print(resp.text)
            time.sleep(5)
