bigqueryexample
===============

Big Query Example

Set up for the first time
===============

1. Have a valid google-cloud-sdk installed on your local machine and
    make sure that the cloud sdk's bin/ folder is in $PATH.
2. Create a virtualenv to contain this project. For example,
    'virtualenv --clear --no-site-packages keyscores-bigquery'
3. Inside the 'keyscores-bigquery' directory:
    $ git clone git@github.com:keyscores/bigqueryexample.git
    $ pip install GoogleAppEngineCloudStorageClient -t bigqueryexample/keyscores

Run the dev server locally
===============

1. Inside the 'keyscores-bigquery' directory:
    $ . bin/activate
    $ ./initialize.sh
    $ ./run_dev_server.sh

Run the curl scripts to test the dev server
===============

1. Inside the 'keyscores-bigquey/bigqueryexample' directory:
    $ . setup_env.sh
    $ cd keyscores/curl_scripts
2. To upload a test file to the dev server
    $ ./upload_file.sh Country_and_Region.xlsx
   To upload a test file to the production server
    $ ./upload_file.sh Country_and_Region.xlsx
