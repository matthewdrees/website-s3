import datetime
import json
import os
import sys
from pathlib import Path
from string import Template
import subprocess

import post

# Output directory
outDir = "out"
postsDir = "posts"

# Copy PhotoSwipe
photoSwipeInDir = "PhotoSwipe/dist"
photoSwipeOutDir = os.path.join(outDir, "photoswipe")
Command(photoSwipeOutDir, photoSwipeInDir, Copy(photoSwipeOutDir, photoSwipeInDir))

env = Environment()


def scrub_filename_for_url(filename):
    """Modify a filename so it is a valid url.

    :rtype: str
    :return filename updated as a valid url
    """
    return filename.replace(" ", "-")


def isimage(filename):
    """Return True if filename has a typical image file extension."""
    _, ext = os.path.splitext(filename)
    return ext.lower() in (".jpg", ".jpeg")


class PostInfo:
    def __init__(self, post_folder_name):
        """Convert post folder name into date, name, and url.

        E.g. post folder name '2020-06-20 Post Name':
        self.date: datetime.date(2020,6,20)
        self.name = 'Post Name'
        self.url = "2020/06/20/post-name"
        self.out_url = "{outDir}/2020/06/20/post-name"
        """
        path_parts = post_folder_name.split(" ", maxsplit=1)
        self.date = datetime.date.fromisoformat(path_parts[0])
        self.name = path_parts[1]
        post_url_name = scrub_filename_for_url(self.name.lower())
        self.url = f"{self.date.year}/{self.date.month}/{self.date.day}/{post_url_name}"
        self.out_url = f"{outDir}/{self.url}"
        self.moviename = f"{post_url_name}.mp4"


class PostImageUrlNames:
    def __init__(self, image_filename):
        """Create url names for generated post images.

        Generate little/medium/big image url names from the source filename.

        :param image_filename: path and filename to original image for the post.
                               e.g. "posts/2020-06-30-june-2020/01 image name.jpg"
        """
        basename, ext = os.path.splitext(scrub_filename_for_url(image_filename))
        self.little = f"{basename}_l{ext}"
        self.medium = f"{basename}_m{ext}"
        self.big = f"{basename}_b{ext}"


def build_post_images(post_in_path, postInfo):
    """Build commands for images."""

    for imagename in os.listdir(post_in_path):
        if not isimage(imagename):
            continue
        postImageUrlNames = PostImageUrlNames(imagename)
        image_in = os.path.join(post_in_path, imagename)
        little_image_out = f"{postInfo.out_url}/{postImageUrlNames.little}"
        medium_image_out = f"{postInfo.out_url}/{postImageUrlNames.medium}"
        big_image_out = f"{postInfo.out_url}/{postImageUrlNames.big}"
        # Creating all 3 images in a single convert command is twice as fast as creating each separately.
        env.Command(
            (little_image_out, medium_image_out, big_image_out),
            image_in,
            (
                f'convert "{image_in}"'
                f" -resize 1600x1600 -write {big_image_out}"
                f" -resize 1024x1024 -write {medium_image_out}"
                f" -resize 240x240 {little_image_out}"
            ),
        )


def get_images_html(image_files):
    """Given a list of image filenames, return image html fragment.

    :param image_files: e.g. ["posts/2020-06-30-june-2020/01 image name.jpeg", ...]
    :return html fragment for $images in post_template.html.
    :rtype: str
    """
    html = []
    for image_file in image_files:
        image_name = os.path.basename(image_file)
        postImageUrlNames = PostImageUrlNames(image_name)

        cp = subprocess.run(
            ["identify", "-format", "%wx%h", image_file],
            capture_output=True,
            universal_newlines=True,
        )
        source_image_dimensions = cp.stdout.strip()
        post_image_dimensions_big = post.getPostImageDimensions(
            source_image_dimensions, 1600, 1200
        )
        post_image_dimensions_medium = post.getPostImageDimensions(
            source_image_dimensions, 1024, 768
        )

        html.append(
            (
                f'<a href="{postImageUrlNames.big}" data-size="{post_image_dimensions_big}"'
                f' data-med="{postImageUrlNames.medium}" data-med-size="{post_image_dimensions_medium}" class="demo-gallery__img--main">'
            )
        )
        html.append(f'<img src="{postImageUrlNames.little}" alt=""/>')
        html.append(
            f"<figure>{post.getImageCaptionFromFilename(image_file)}</figure></a>"
        )

    return "\n".join(html)


def write_post_index_html(target, source, env):
    """Build command for post index.html.

    :param source: list of depencency source files:
        ['post_template.html',
         'posts/2020-06-30-june-2020/a.json',
         'posts/2020-06-30-june-2020/01 name.jpg',
         'posts/2020-06-30-june-2020/02 name.jpg',
         'posts/2020-06-30-june-2020/03 name.jpg',
         ...
         'out/2020/6/3/30/june-2020/june-2020.mp4']
    """
    d = {}  # template substitute dictionary
    image_files = []  # list of images in 'source' list
    for s in source:
        filename = str(s)
        if isimage(filename):
            image_files.append(filename)
        elif os.path.basename(filename) == "a.json":
            with open(filename, "r") as f:
                j = json.load(f)
                d["blurb"] = j["blurb"]
            p = Path(filename)
            postInfo = PostInfo(p.parts[-2])
            d["title"] = postInfo.name
            d["moviename"] = postInfo.moviename
    d["images"] = get_images_html(image_files)

    # Write post index.html with substitutions from a template.
    with open("post_template.html", "r") as f:
        html_template = Template(f.read())
    with open(str(target[0]), "w") as f:
        f.write(html_template.substitute(d))


def build_post_index_html(post_in_path, postInfo):
    """Build post index.html."""

    post_index_html_out = f"{postInfo.out_url}/index.html"
    source = ["post_template.html"]

    # Add all files in post directory as a source dependency
    for f in os.listdir(post_in_path):
        source.append(os.path.join(post_in_path, f))

    env.Command(post_index_html_out, source, write_post_index_html)


def build_post_mp4(post_in_path, postInfo):
    """Build post movie file"""
    source = os.path.join(post_in_path, postInfo.moviename)
    if os.path.isfile(source):
        target = f"{postInfo.out_url}/{postInfo.moviename}"
        env.Command(target, source, "ffmpeg -i $SOURCE -vf scale=-2:416 $TARGET")


def build_sidebar_html(target, source, env):
    """Build sidebar.html"""
    post_folder_names = [Path(str(s)).parts[-1] for s in source]

    html = ["<nav>", "<ul>"]
    curYear = 0
    for post_folder_name in post_folder_names:
        p = PostInfo(post_folder_name)
        if p.date.year != curYear:
            curYear = p.date.year
            html.append(f'<li id="year">{curYear}</li>')
        html.append(f'<li><a href="../../../../{p.url}/index.html">{p.name}</a></li>')
    html.append("</ul>")
    html.append("</nav>")

    with open(str(target[0]), "w") as f:
        f.write("\n".join(html))


def do_sidebar_html(post_folder_names):
    """Set up dependencies for sidebar.html

    :param post_folder_names: sorted list of 2020-06-30-post-name folder names.
    :rtype: None
    """
    target = os.path.join(outDir, "sidebar.html")
    source = [os.path.join(postsDir, p) for p in post_folder_names]
    env.Command(target, source, build_sidebar_html)


def do_robots_txt():
    """Create robots.txt file."""
    source = "robots.txt"
    target = os.path.join(outDir, source)
    Command(target, source, Copy("$TARGET", "$SOURCE"))


def do_site_css():
    source = "site.css"
    target = os.path.join(outDir, source)
    Command(target, source, Copy("$TARGET", "$SOURCE"))


# List of post folder names (skip lame hidden folders)
post_folder_names = sorted([f for f in os.listdir(postsDir) if not f.startswith(".")])

# Process individual posts.
for post_folder_name in post_folder_names:

    post_in_path = os.path.join(postsDir, post_folder_name)
    postInfo = PostInfo(post_folder_name)

    build_post_images(post_in_path, postInfo)
    build_post_index_html(post_in_path, postInfo)
    build_post_mp4(post_in_path, postInfo)

# sidebar.html
do_sidebar_html(post_folder_names)

# site.css
do_site_css()

# robots.txt
do_robots_txt()