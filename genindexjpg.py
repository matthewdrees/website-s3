import argparse
import json
import os
import shutil

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Create part of mattandcress.com.')
    parser.add_argument('--input', metavar='content/2014/april/a.json', dest='input',
                        help='Input config json file.')
    parser.add_argument('--output', metavar='mac/2014/april/index.jpg', dest='output',
                        help='Output jpg file.')

    args = parser.parse_args()

    with open(args.input, 'r') as f:
        j = json.load(f)

    content_path = os.path.dirname(args.input)
    
    shutil.copyfile(os.path.join(content_path, 'images', j['index image']),
                    args.output)
