import cloudstorage as gcs


def is_content_type_excel(content_type):
    """
    :param content_type: a Content-Type string value
    :return: True if content_type indicates an Excel file; False otherwise.
    """
    if content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or \
            content_type == 'application/vnd.ms-excel':
        return True
    return False


def write_gcs_file(gcs_filename, data, content_type):
    """
    :param gcs_filename: a gcs file path that looks like "/bucket/filename"
    :param data: a buffer of data to write to the gcs file
    """
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(
        gcs_filename, mode='w', content_type=content_type,
        retry_params=write_retry_params
    )
    gcs_file.write(data)
    gcs_file.close()
