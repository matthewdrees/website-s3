import datetime
import os
from pathlib import Path

# Output directory
outDir = 'out'
postsDir = 'posts'

# Copy PhotoSwipe
photoSwipeInDir = 'PhotoSwipe/dist'
photoSwipeOutDir = os.path.join(outDir, 'photoswipe')
Command(photoSwipeOutDir, photoSwipeInDir, Copy(photoSwipeOutDir, photoSwipeInDir))

env = Environment()

def scrub_filename_for_url(filename):
    '''Modify a filename so it is legal in a url.

    :rtype: str
    :return filename updated as a legal url
    '''
    return filename.replace(' ','-')

class PostInfo:
    def __init__(self, post_folder_name):
        '''Convert post folder name into date, name, and url.

        E.g. post folder name '2020-06-20 Post Name':
        self.date: datetime.date(2020,6,20)
        self.name = 'Post Name'
        self.url = "2020/06/20/post-name"
        '''
        path_parts = post_folder_name.split(' ', maxsplit=1)
        self.date = datetime.date.fromisoformat(path_parts[0])
        self.name = path_parts[1]
        post_url_name = scrub_filename_for_url(self.name.lower())
        self.url = f"{outDir}/{self.date.year}/{self.date.month}/{self.date.day}/{post_url_name}"

def build_post_images(post_in_path, postInfo):
    '''Build commands for images.'''

    for imagename in os.listdir(post_in_path):
        scrubbed_image_name = scrub_filename_for_url(imagename)
        basename, ext = os.path.splitext(scrubbed_image_name)
        print(ext)
        if ext.lower() not in ('.jpg', '.jpeg'):
            continue
        image_in = os.path.join(post_in_path, imagename)
        print(image_in)
        partial_image_out = f"{postInfo.url}/{basename}"
        small_image_out = f"{partial_image_out}_l{ext}"
        medium_image_out = f"{partial_image_out}_m{ext}"
        big_image_out = f"{partial_image_out}_b{ext}"
        # Creating all 3 images in a single convert command is twice as fast as creating each separately.
        env.Command((small_image_out, medium_image_out, big_image_out), image_in,
            (f'convert "{image_in}"'
             f' -resize 240x240 -write {small_image_out}'
             f' -resize 1024x1024 -write {medium_image_out}'
             f' -resize 1600x1600 {big_image_out}'))

# Do individual posts
posts = os.listdir(postsDir)
for post_folder_name in posts:

    # Skip hidden folders
    if post_folder_name.startswith('.'):
        continue

    #print(post)
    post_in_path = os.path.join(postsDir, post_folder_name)
    postInfo = PostInfo(post_folder_name)
    # ... the dates all become part of the output url: 'yyyy/mm/dd/post-name'
    print(postInfo.url)
    build_post_images(post_in_path, postInfo)

    # Do the images
    # post index.html dependency.

    # post mp4 dependency.

    # post pics dependency.

