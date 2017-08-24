#!/usr/bin/python

from resizer import run
from resizer.event_parser import parse_from
from resizer.exceptions import BaseLambdaResponse


def entrypoint(event, _):
    '''
    This is where our Lambda is called by AWS
    '''
    try:
        run(parse_from(event))
    except BaseLambdaResponse as response:
        return response.get()


# Only run from command line (simulate Lambda execution)
if __name__ == '__main__':
    import logging, sys
    root = logging.getLogger()
    root.addHandler(logging.StreamHandler(sys.stdout))
    stub_data = {
        "path": "/500x500/0000000d2fb81cf34e3ef2b95d14b1f7ec88d2ce3a139e7ee98b324c337252da/irony.jpeg",
        "qs": None,
        "headers": {
            "Via": "2.0 370d746a5e665df83579975d079783ed.cloudfront.net (CloudFront)",
            "Accept-Language": "en,pt-BR;q=0.8,pt;q=0.6,es;q=0.4,he;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Forwarded-Proto": "https",
            "X-Forwarded-For": "203.17.253.249, 54.239.202.65",
            "CloudFront-Viewer-Country": "AU",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "upgrade-insecure-requests": "1",
            "X-Amzn-Trace-Id": "Root=1-599e210d-65447dc94fc26e8676795a5d",
            "dnt": "1",
            "Host": "xlpfm1e182.execute-api.ap-southeast-2.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "svC8pNQJVdfQt1es2aI31vGNP_kLm6s7vsKVmoBkDmfJ2v3bRYIfUQ==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "X-Forwarded-Port": "443",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-Desktop-Viewer": "true"
        }
    }
    entrypoint(stub_data, None)
