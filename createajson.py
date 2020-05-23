import json
import os
import shutil
import sys
from natsort import natsorted

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print('Usage: $ python3 createajson.py content/2016/folder')
        print('This creates a pre-populated a.json file in that folder based on images.')
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.exists(path):
        print("Path %s doesn't exist." % path)
        sys.exit(1)

    ajson_path = os.path.join(path, 'a.json')
    if os.path.exists(ajson_path):
        print("Path '%s' already exists." % ajson_path)
        sys.exit(1)

    # photos app exports jpgs sequential like this:
    #  "photo - 1"
    #  "photo - 2"
    #  ...
    #  "photo - 9"
    #  "photo - 10"
    #  "..."
    #
    # Have to do 2 corrections:
    #  - Remove the spaces " - " -> "_".
    #  - Use natsort to handle single/double digits in name.
    jpg_filenames = os.listdir(os.path.join(path, 'images'))
    jpg_filenames = natsorted(jpg_filenames)
    new_jpg_filenames = []
    for jpeg_filename in jpg_filenames:
        new_jpg_filename = jpeg_filename.replace(' - ', '_')
        shutil.move(os.path.join(path, 'images', jpeg_filename),
                    os.path.join(path, 'images', new_jpg_filename))
        new_jpg_filenames.append(new_jpg_filename)

    print(new_jpg_filenames)

    j = {}
    j['images'] = []
    for jpg in new_jpg_filenames:
        j['images'].append({'caption': '', 'image': jpg})
        print('Found picture: %s' % jpg)
    j['index image'] = ''
    j['blurb'] = ''
    j['date'] = ''
    j['title'] = ''

    with open(ajson_path, 'w') as f:
        json.dump(j, f, indent=2)
        print('Created file: %s' % ajson_path)

