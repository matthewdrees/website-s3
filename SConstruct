import datetime
import os

# Output directory
outDir = 'out'

# Copy PhotoSwipe
photoSwipeInDir = 'PhotoSwipe/dist'
photoSwipeOutDir = os.path.join(outDir, 'photoswipe')
Command(photoSwipeOutDir, photoSwipeInDir, Copy(photoSwipeOutDir, photoSwipeInDir))

env = Environment()

class PostDateAndName:
    def __init__(self, post_folder_name):
        # Post folders are labelled 'yyyy-mm-dd Post Name' so split on the first space.
        path_parts = post_folder_name.split(' ', maxsplit=1)
        print(path_parts[0])
        self.date = datetime.date.fromisoformat(path_parts[0])
        self.post_name = path_parts[1]

    def getDateAsUrlPath(self):
        return f"{self.date.year}/{self.date.month}/{self.date.day}"

# Do individual posts
posts = os.listdir('posts')
for post_folder_name in posts:

    # Skip hidden folders
    if post_folder_name.startswith('.'):
        continue

    #print(post)
    post_in_path = os.path.join('posts', post_folder_name)
    postDateAndName = PostDateAndName(post_folder_name)
    # ... the dates all become part of the output url: 'yyyy/mm/dd/post-name'
    post_out_path = os.path.join(outDir, postDateAndName.getDateAsUrlPath())
    #print(post_out_path)
    #print(postDateAndName.post_name)

    # post index.html dependency.

    # post mp4 dependency.

    # post pics dependency.

