# Build the base images:

1. make sure docker is installed

```bash
    # build only python image
    python upload_to_hub.py -i python

    # build all images
    python upload_to_hub.py -i all

```

# Notes:

base images must have the gritty repo installed, and python2 and nodejs
