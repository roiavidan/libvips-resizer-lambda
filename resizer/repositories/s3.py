import logging

from boto3 import client
from botocore.exceptions import ClientError

from resizer.exceptions import BucketNotFoundResponse, FileNotFoundResponse, InternalErrorResponse
from resizer.timing import record_run_time_for


logger = logging.getLogger()
logger.setLevel(logging.INFO)


@record_run_time_for(name='s3')
def get_image(bucket, key):
    logger.info('Fetching image "{0}" from "{1}"'.format(key, bucket))

    try:
        response = client('s3').get_object(Bucket=bucket, Key=key)
        image_data = response['Body'].read()

        logger.info('Retrieved {0} bytes for "{1}"'.format(len(image_data), key))
        return image_data
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            raise BucketNotFoundResponse(e.response['Error']['BucketName'])
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise FileNotFoundResponse(bucket, e.response['Error']['Key'])
        raise InternalErrorResponse(str(e))
    except Exception as e:
        raise InternalErrorResponse(str(e))
