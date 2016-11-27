import json
import os
import sys

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

    jpgs_path = os.path.join(path, 'images')
    jpgs = []
    for (dirpath, dirnames, filenames) in os.walk(jpgs_path):
        jpgs.extend([f for f in filenames if f[-3:] == 'jpg'])
        break
            
    print(jpgs)

    j = {}
    j['images'] = []
    for jpg in jpgs:
        j['images'].append({'caption': '', 'image': jpg})
        print('Found picture: %s' % jpg)
    j['index image'] = ''
    j['blurb'] = ''
    j['date'] = ''
    j['title'] = ''

    with open(ajson_path, 'w') as f:
        json.dump(j, f, indent=2)
        print('Created file: %s' % ajson_path)

