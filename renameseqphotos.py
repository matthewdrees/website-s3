import argparse
import os
import shutil

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Rename stupid sequential photo naming from photos app.')
    parser.add_argument('--dir', metavar='content/path', dest='directory',
                        help='Path to images to rename.')

    args = parser.parse_args()

    for fn in os.listdir(args.directory):
        fn = os.path.join(args.directory, fn)
        if ' - ' in fn:
            print(fn)
            shutil.move(fn, fn.replace(' - ', '_'))




