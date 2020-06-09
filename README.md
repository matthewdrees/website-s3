# website-s3
Creating and publishing family website for pictures and movies.

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

Create a folder:

    $ mkdir content/2020/new

Put images in an "images" subfolder. I put full resolution images, they get resized down to what's appropriate for putting on the site.

    $ mkdir content/2020/new/images
    ... copy imges

I use iMovie to create a 1280x720 mp4 movie. I name the movie the same as the folder name.

    content/2020/new/new.mp4

Use the createajson.py script in the running docker instance to create a skeleton a.json file for text content and information to create web page artifacts.

    # python createajson content/2020/new

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

## Sync with amazon s3:
    # python syncs3.py
