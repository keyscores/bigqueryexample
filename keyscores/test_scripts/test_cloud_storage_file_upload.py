import os
import unittest

import requests


file_names = [
    'Country_and_Region.xlsx', 'Sales.xlsx',
    'Comission_and_Tax.xlsx', 'Currency.xlsx'
]


class ExcelFileLoadingTestCase(unittest.TestCase):
    def setUp(self):
        super(ExcelFileLoadingTestCase, self).setUp()
        self.server_url = os.environ['SERVER_URL']
        self.bucket_name = os.environ['BUCKET_NAME']
        self.content_type = os.environ['CONTENT_TYPE']

    def test_upload_files_to_cloud_storage(self):
        for filename in file_names:
            filepath = os.path.join(
                os.path.dirname(__file__),
                filename
            )
            with open(filepath, 'r') as f:
                r = requests.post(
                    os.path.join(self.server_url, "upload"),
                    data=f,
                    headers={
                        'X-Keyscores-Filename': filename,
                        'X-Keyscores-Bucket-Name': self.bucket_name,
                        'Content-Type':self.content_type
                    }
                )
                self.assertEqual(r.status_code, 200)
