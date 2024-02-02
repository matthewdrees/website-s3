# website-s3

Creating and publishing family website with pictures and movies using Amazon S3.

I'M NO LONGER USING OR MAINTAINING THIS REPOSIORY. But I'm leaving it as a reference for now.

## How to run with the compiler/setup from the docker container.

This will build a docker image:

    $ docker build -t website-s3 .

After building once, this will run interactively using host side source code
instead of what's in the image (so you can edit and use source control in
another terminal, and build/run in this one):

    $ docker run --mount type=bind,source=$(pwd),target=/app -i -t website-s3 /bin/sh

If you exited that container and want to reconnect:

    $ docker ps
    $ docker exec -it <container name> /bin/sh

I use Docker Desktop to monitor the running docker containers.

## How to add images and movies

Create post folder:

    $ cd posts
    $ mkdir 2020-04-06-imma-post

Put images in the post folder. I use the Photos app on my mac, select the photos, and export them to the post folder. Notes:
* I use resolution images, they get resized appropriately later.
* For "File Naming" I use "sequential" so the photos show up in chronological order.

You can optionally change the name of each file to be the caption of the photo.

    $ mv "1.jpeg" "01 this is a caption.jpeg"

I use iMovie to create a 1280x720 mp4 movie. I name the movie the same as the folder name.

    imma-post.mp4

Use the createajson.py script in the running docker instance to create a skeleton a.json file for text content and information to create web page artifacts.

    # python createajson.py content/2020/new

Edit the newly created a.json file for captioning images, date of post, blurb, etc.

    $ vim content/2020/new/a.json

## Create output folder, generate movie, image, and html files: (todo, get scons to automate this)

    # mkdir out/2020/new
    # ffmpeg -i content/2020/new/new.mp4 -vf scale=-2:480 out/2020/new/new.mp4
    # ffmpeg -i content/2020/new/new.mp4 -c:v libvpx-vp9 -b:v 0 -crf 30 -vf scale=-2:480 -pass 1 -an -f webm /dev/null -y
    # ffmpeg -i content/2020/new/new.mp4 -c:v libvpx-vp9 -b:v 0 -crf 30 -vf scale=-2:480 -pass 2 -c:a libopus out/2020/new/new.webm
    # rm ffmpeg2pass-0.log
    # python genfolderindex.py --inputpath content/2020/new --outputpath out/2020/new
    # python genindex.py --input content --output out

## Run the website locally

    // TODO: put in the container
    $ cd out
    $ http-server

## Install aws cli (first time setup only)

    // Todo: put in container.
    - Install aws cli.
    - Configure access: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

## Sync with amazon s3:

    # cd out
    # aws s3 sync . s3://your.s3.uri --acl public-read --storage-class REDUCED_REDUNDANCY --exclude "*.DS_Store" --delete

