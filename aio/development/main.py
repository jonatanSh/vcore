"""

Important notes:

1. this script is intended to run for python==2.7 and above

2. this script will write some permanent settings

3. don't split the script into modules.

"""
import shutil
import os
import subprocess
import optparse
import sys
import json
import subprocess
import atexit


class Settings(object):
    def __init__(self):
        self.settings_object = None
        self.path = "settings.json.ignore"

        # load or make settings
        self.load_or_make()

    def load_or_make(self):
        if not os.path.exists(self.path):
            with open(self.path, "w+") as settings:
                json.dump({
                    "install_termcolor": True,
                }, settings)
        with open(self.path, "r") as settings:
            self.settings_object = json.load(settings)

    def save(self):
        with open(self.path, "w+") as settings:
            json.dump(self.settings_object, settings)

    def get_setting(self, name):
        return self.settings_object[name]

    def set_setting(self, name, value):
        self.settings_object[name] = value


settings = Settings()


# intend to work only with python ! (out of the box, -> no requirements)
class Printer(object):
    def __init__(self):
        self.max_length = 120
        self.indent = 0
        self.pointer = ""
        self.title = False
        printer_wrapper = None
        try:
            from termcolor import colored
            printer_wrapper = colored
        except ImportError:
            try:
                if not settings.get_setting("install_termcolor"):
                    raise ImportError()
                if not self.ask("module for enhanced gui not found, install it"):
                    print("skipping installation of enhanced gui")

                    settings.set_setting("install_termcolor", False)
                    settings.save()

                    # write to make it persistent
                    raise ImportError()

                import pip
                pip.main(["install", "termcolor"])
                from termcolor import colored
                printer_wrapper = colored
            except Exception:
                pass

        if not printer_wrapper:
            self.printer_wrapper = self.default_printer_wrapper
        else:
            self.printer_wrapper = printer_wrapper

    def default_printer_wrapper(self, message, *args):
        return message

    def ask(self, question):
        val = input("{0} Y/n?".format(question))
        return val.lower() != "n"  # notation for default true

    def _print(self, *args, **kwargs):
        args = [self.pointer] + list(args)
        message = "".join(args)
        print("{0}{1}".format(" " * self.indent, self.printer_wrapper(message, **kwargs)))

    def print(self, *args, **kwargs):
        current_printer = self._print

        if self.title:
            current_printer = self.print_title

        current_printer(*args, **kwargs)

    def print_title(self, *args, **kwargs):
        message = "".join(args)
        p_len = min(self.max_length, len(message) + 8)
        self._print("@" * p_len, **kwargs)
        self._print("{0}   {1}   {0}".format("@", message), **kwargs)
        self._print("@" * p_len, **kwargs)

    def green(self, *args):
        self.print(*args, color="green")

    def blue(self, *args):
        self.print(*args, color="blue")

    def red(self, *args):
        self.print(*args, color="red")

    def yellow(self, *args):
        self.print(*args, color="yellow")

    def start_print(self, title=False, indent=0, pointer=""):
        self.title = title
        self.indent = indent
        self.pointer = pointer

    def end_print(self, title=False, indent=0, pointer=""):
        self.title = title
        self.indent = indent
        self.pointer = pointer


printer = Printer()


# the parser changes this options
class RuntimeOptions(object):
    FORCE_OVERRIDE = False


class WebImage(object):
    IMAGE_NAME = "challenge_framework/web"
    TAG = "development"
    location = "web"

    @staticmethod
    def init():
        printer.yellow("Copying ../python-req.txt to web/.")
        shutil.copy("../python-req.txt", "web/.")

    @staticmethod
    def cleanup():
        printer.yellow("Starting clean up")
        os.remove("web/python-req.txt")


class HostImage(object):
    IMAGE_NAME = "challenge_framework/docker_host"
    TAG = "development"
    location = "host"

    @staticmethod
    def init():
        printer.yellow("Copying ../python-req.txt to host/.")
        shutil.copy("../python-req.txt", "host/.")

    @staticmethod
    def cleanup():
        printer.yellow("Starting clean up")
        os.remove("host/python-req.txt")


IMAGES = [
    WebImage,
    # HostImage
]


def clean_build(settings):
    os.system("docker rmi -f {0}:{1}".format(settings.IMAGE_NAME, settings.TAG))


def build_required(settings):
    stdout, stderr = subprocess.Popen("docker images -a".split(" "), stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE).communicate()

    stdout = stdout.decode("utf-8")
    return not (settings.IMAGE_NAME in stdout) or RuntimeOptions.FORCE_OVERRIDE


def build(settings):
    printer.start_print(title=True)
    printer.blue("Building image: ", settings.IMAGE_NAME)
    printer.end_print()

    printer.start_print(indent=3, pointer="----> ")
    settings.init()
    ecode = subprocess.call("docker build -t {0}:{1} .".format(settings.IMAGE_NAME, settings.TAG).split(" "),
                            cwd=os.path.join(os.getcwd(), settings.location))

    settings.cleanup()

    printer.end_print()

    if ecode:
        printer.start_print(title=True)
        printer.red("error occurred make sure docker, docker-compose is installed")
        printer.end_print()
        return False
    else:
        return True


def start():
    printer.start_print(title=True)
    printer.green("Starting everything and displaying logs")
    printer.end_print(title=False)
    os.system("docker-compose up")


def parse():
    parser = optparse.OptionParser()

    parser.add_option("-f", "--force-rebuild",
                      help="remove the old environment and rebuild it", action="store_true", dest="force_override",
                      default=False)

    options, args = parser.parse_args()

    RuntimeOptions.FORCE_OVERRIDE = options.force_override


def runserver():
    printer.start_print(title=True)
    printer.blue("Running challenge framework: https://github.com/jonatanSh/challenge-framework")
    printer.end_print(title=False)
    ok_to_start = True
    for setting in IMAGES:
        if build_required(setting):
            clean_build(setting)
            ok_to_start = build(setting)
            printer.start_print(title=True)
            printer.green("Done building:", setting.IMAGE_NAME)
            printer.end_print(title=False)
    if ok_to_start:
        start()
    else:
        printer.start_print(title=True)
        printer.red("Not starting error ...")
        printer.end_print(title=False)


DOCKER_HOST = None

if __name__ == "__main__":
    # parsing and settings up RuntimeOptions
    parse()
    if len(sys.argv) > 1:
        if sys.argv[1] != "runserver":
            os.system("python run_command.py {0}".format(" ".join(sys.argv[1:])))
        else:
            runserver()
    else:
        os.system("python run_command.py --help")


def exit_func():
    DOCKER_HOST.terminate()


atexit.register(exit_func)
