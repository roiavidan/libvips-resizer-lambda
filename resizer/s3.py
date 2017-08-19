import boto3, botocore, tempfile

def download(bucket, key):
    s3 = boto3.resource('s3')
    with tempfile.NamedTemporaryFile(delete=False) as f:
        s3.Bucket(bucket).download_file(key, f.name)
        return f
