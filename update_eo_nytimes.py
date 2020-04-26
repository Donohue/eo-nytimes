#!/usr/bin/env python
from __future__ import print_function

import argparse
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from datetime import datetime
import os
import requests
import subprocess
import sys

from electric_objects import ElectricObjects

def download_nytimes_frontpage(date):
    with open('/tmp/scan.pdf', 'wb') as f:
        dt = date.strftime('%Y/%m/%d')
        print('Downloading NYTimes frontpage for %s' % dt)
        url = 'https://static01.nyt.com/images/%s/nytfrontpage/scan.pdf' % dt
        r = requests.get(url)
        f.write(r.content)
        print('Wrote NYTimes frontpage to %s' % f.name)

def convert_nytimes_image():
    print('Converting NYTimes frontpage to JPEG')
    args = ['convert', '-resize', '1260x', '/tmp/scan.pdf', '/tmp/scan.jpg']
    data = subprocess.check_output(args)
    print('Completed conversion')
    return data

def _key_for_date(date):
    return date.strftime('%Y/%m/%d/scan.jpg')

def image_already_exists(bucket, date):
    return bucket.get_key(_key_for_date(date)) != None

def image_url(bucket, date, region='us-west-2'):
    return 'https://%s.s3-%s.amazonaws.com/%s' % (bucket.name, region, _key_for_date(date))

def save_to_bucket(bucket, date, region='us-west-2'):
    print('Uploading to S3')
    key = Key(bucket)
    key.key = _key_for_date(date)
    key.set_contents_from_filename('/tmp/scan.jpg')
    print('Completed upload to S3')

if __name__ == '__main__':  
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', default=datetime.today().strftime('%Y-%m-%d'), help='Date of NYTimes homepage to update', type=lambda d: datetime.strptime(d, '%Y-%m-%d'))
    parser.add_argument('--user', required=True, help='EO username')
    parser.add_argument('--password', required=True, help='EO password')
    parser.add_argument('--device', required=True, help='EO device ID')
    parser.add_argument('--bucket', required=True, help='S3 bucket name')
    parser.add_argument('--region', default='us-west-2', help='AWS region for S3 bucket')
    args = parser.parse_args()

    aws_access_token = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_access_token_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
    if not aws_access_token or not aws_access_token_secret:
        print('Missing AWS credentials. Please set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables')
        parser.print_help()
        sys.exit(-1)
	
    conn = S3Connection(aws_access_token, aws_access_token_secret)
    bucket = conn.get_bucket(args.bucket)
    eo = ElectricObjects(args.user, args.password)
    
    url = image_url(bucket, args.date, region=args.region)
    if not image_already_exists(bucket, args.date):
        download_nytimes_frontpage(args.date)
        convert_nytimes_image()
        save_to_bucket(bucket, args.date, region=args.region)
    else:
        print('Image already exists in S3 for %s' % args.date.strftime('%Y-%m-%d'))

    print('Updating EO URL to %s' % url)
    eo.set_url(url, args.device)
    print('Completed update')
