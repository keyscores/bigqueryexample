import os

import cloudstorage as gcs
import webapp2

from google.appengine.api import app_identity


class ImportDataHandler(webapp2.RequestHandler):
    def post(self):
        bucket_name = self.request.headers.get(
            'X-Keyscores-Bucket-Name',
            app_identity.get_default_gcs_bucket_name()
        )
        bucket = '/' + bucket_name
        filename = self.request.headers['X-Keyscores-Filename']
        gcs_filename = os.path.join(bucket, filename)
        content_type = self.request.headers['Content-Type']
        file_data = self.request.body
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(
            gcs_filename, mode='w', content_type=content_type
        )
        gcs_file.write(file_data)
        gcs_file.close()


application = webapp2.WSGIApplication([
    ('/upload', ImportDataHandler)
], debug=True)
