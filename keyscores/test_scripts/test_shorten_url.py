import json
import os
import unittest

import requests

testing_project_id = 'kinetic-physics-644'


class URLShortnerTestCase(unittest.TestCase):
    def test_url_shortner(self):
        # GET the shortned URL of a long url through
        # the endpoint /shorten_url
        server_url = os.environ['SERVER_URL']
        url = os.path.join(server_url, 'shorten_url')
        resp = requests.get(
            url, params={
                'long_url': 'https://developers.google.com/appengine/docs/python/appidentity/#Python_Asserting_identity_to_Google_APIs'
            },
            headers={
                'X-Keyscores-Project-Id': testing_project_id
            }
        )
        self.assertEqual(resp.status_code, 200)
