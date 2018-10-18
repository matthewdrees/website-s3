# website-s3
Creating and publishing family website for pictures and movies.

## How to run with the compiler/setup from the docker container.

This will build a docker image:

    $ docker build -t website-s3 .

After building once, this will run interactively using host side source code
instead of what's in the image (so you can edit and use source control in
another terminal, and build/run in this one):

    $ docker run --mount type=bind,source=$(pwd),target=/app -i -t website-s3 /bin/sh

Take notice if your images are stacking up:

    $ docker image ls

... and prune them if necessary:

    $ docker system prune
