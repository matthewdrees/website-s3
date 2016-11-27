'''Sync files to s3 bin.
'''
import argparse
import datetime
import logging
import json
import os
import sys

from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.s3.key import Key
from boto import utils

def getHeaders(key_name):
    headers = {}
    extension = os.path.splitext(key_name)[1]
    if extension == "ogv":
        headers["Content-Type"] = "application/ogg"

def sync(config, dry_run):
    
    conn = S3Connection(config['access_key_id'],
                        config['aws_secret_access_key'],
                        calling_format=OrdinaryCallingFormat())
    b = conn.get_bucket(config['bucket_name'])

    logging.info("Getting key timestamps...")
    
    s3KeyDts = {}

    # key_name: e.g. 2013/sanjuanislands/index.html
    for key in b.list():
        if key.name[-len('$folder$'):] != '$folder$':
            s3KeyDts[key.name] = utils.parse_ts(key.last_modified)

    logging.info("Walking files...")
    
    os.chdir("out")
    for path, _, filenames in os.walk("."):
        path = path[2:]
        for filename in filenames:
    
            if filename[0] == ".":
                continue
            
            key_name = os.path.join(path, filename)
            
            if key_name in s3KeyDts:
                
                fileDt = datetime.datetime.utcfromtimestamp(os.path.getmtime(key_name))

                if fileDt <= s3KeyDts[key_name]:
                    
                    logging.debug("'%s' - File up to date. Skipping. %s <= %s" % (key_name, str(fileDt), str(s3KeyDts[key_name])))
                    
                else:
                        
                    logging.info("'%s' - File out of date. Replacing. %s > %s" % (key_name, str(fileDt), str(s3KeyDts[key_name])))
                    if not dry_run:
                        key = Key(b, key_name)
                        key.set_contents_from_filename(key_name,
                                                     headers=getHeaders(key_name),
                                                     replace=True,
                                                     cb=None,
                                                     num_cb=10,
                                                     policy="public-read",
                                                     md5=None,
                                                     reduced_redundancy=True,
                                                     encrypt_key=False)
                
                del s3KeyDts[key_name]
            
            else:
                
                logging.info("'%s' - new file! Adding." % key_name)
                if not dry_run:
                    key = Key(b, key_name)
                    key.set_contents_from_filename(key_name,
                                                 headers=getHeaders(key_name),
                                                 replace=True,
                                                 cb=None,
                                                 num_cb=10,
                                                 policy="public-read",
                                                 md5=None,
                                                 reduced_redundancy=True,
                                                 encrypt_key=False)
                
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description='sync s3 bucket with contents from "out/" folder.')
    parser.add_argument('--config-file', dest='config_file', default='config.json',
            help='config file for s3 connection information')
    parser.add_argument('--dry-run', dest='dry_run', action='store_true',
            help='Do not actually sync to s3, but show what would be synced.')

    args = parser.parse_args()

    with open(args.config_file, 'r') as f:
        config = json.load(f)

    sync(config, args.dry_run)
    
