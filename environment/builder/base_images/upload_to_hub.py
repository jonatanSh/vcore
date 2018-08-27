#!/usr/bin/python
from optparse import OptionParser
import sys
import os
from subprocess import Popen, call


class Config(object):
    Path = os.getcwd()
    BUILD_FAILURE = 1


parser = OptionParser()

parser.add_option("-i", "--image-name",
                  help="The image name, for example python, for all use all", dest="image_name", default=None)

required_options = [
    {"var": 'image_name', "name": "-i, --image-name"},
]


def get_all_images():
    return [
        os.path.join(Config.Path, dpath, "Dockerfile") for dpath in os.listdir(Config.Path) if os.path.isdir(dpath)
    ]


def popen(call_args):
    out, err = Popen(call_args).communicate()
    if out:
        out = out.decode("utf-8")
    if err:
        err = err.decode("utf-8")
    if err:
        sys.stdout.write("cmd was = {}\n".format(" ".join(call_args)))
        sys.stdout.write("Error out = {}, err = {}\n".format(out, err))
        sys.exit(Config.BUILD_FAILURE)
    if out:
        print(out)


def main(config):
    call("docker login".split(" "))
    if config['image_name'] == 'all':
        build = get_all_images()
    else:
        build = [os.path.join(Config.Path, config['image_name'], "Dockerfile")]

    for build_option in build:
        name = os.path.basename(os.path.dirname(build_option))
        build_name = "{}_{}".format(name, "challenge_framework_base")
        print("Building: {}".format(name))
        # each line must end with space !
        build_args = "docker build {build_path} -t {build_name}".format(
            build_path=os.path.dirname(build_option),
            build_name=build_name
        ).split(" ")
        popen(build_args)
        print("Tagging")
        popen("docker tag {0} jonatansh/challenge_framework:{1}".format(build_name, name).split(" "))

        print("Uploading the image")
        popen("docker push jonatansh/challenge_framework:{}".format(name).split(" "))


if __name__ == '__main__':
    (options, args) = parser.parse_args()
    options = vars(options)
    for option in required_options:
        if not options.get(option['var']):
            parser.error("parameter %s required" % option['name'])

    main(options)
