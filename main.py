from subprocess import Popen, PIPE, call
import sys
import os
import atexit
import pymongo
from environment.utils import settings
import pika
from threading import Thread
from shutil import rmtree
from time import sleep
import optparse
from copy import copy


def path(*args):
    return os.path.join(os.getcwd(), *args)


def p_open_wrapper(**kwargs):
    p = Popen(**kwargs)
    processes.append(p)
    out, err = p.communicate()
    if out:
        out = out.decode('utf-8')
    if err:
        err = err.decode('utf-8')
    print("Call error, kwargs={}, stdout={}, stderr={}".format(kwargs,
                                                               out, err))


def p_call_wrapper(**kwargs):
    p = call(**kwargs)
    processes.append(p)


class RuntimeSettings(object):
    START_PROCESSES = []
    STRATEGIES = {
        "Popen": Popen,
        "call": call,
        "p_open_wrapper": p_open_wrapper,
        "p_call_wrapper": p_call_wrapper
    }
    AVILABLE_PROCESSES = [
        "builder",
        "runner",
        "indexer",
        "docker-host",
        "web",
        "all"
    ]


def get_clean_args():
    args = sys.argv[1:]
    for arg in RuntimeSettings.AVILABLE_PROCESSES:
        arg = "--{0}".format(arg)
        if arg in args:
            args.remove(arg)
    return args


processes_settings = {
    "builder": {"kwargs": {"args": ["python3", path("environment/builder/builder.py")],
                           "cwd": os.path.join(os.getcwd(), 'environment')}, "stdout": PIPE, "stdin": PIPE,
                "stderr": PIPE},
    "indexer": {"kwargs": {"args": ["python3", path("environment/indexer.py")],
                           "cwd": os.path.join(os.getcwd(), 'environment'),
                           "stdout": PIPE, "stdin": PIPE, "stderr": PIPE}},
    "runner": {"kwargs": {"args": ["python3", path("environment/runner.py")],
                          "cwd": os.path.join(os.getcwd(), 'environment'),
                          "stdout": PIPE, "stdin": PIPE, "stderr": PIPE}},
    "web": {"kwargs": {"args": ["python3", path("challenge_framework/manage.py")] + get_clean_args(),
                       "cwd": path("challenge_framework")}, "strategy": "p_call_wrapper"},
    "docker-host": {"kwargs": {"args": ["python3", path("environment/docker/docker_host/main.py")],
                               "cwd": os.path.join(os.getcwd(), 'environment'),
                               "stdout": PIPE, "stdin": PIPE, "stderr": PIPE}},
}


def parse():
    keys = copy(RuntimeSettings.AVILABLE_PROCESSES)
    keys.remove("all")

    parser = optparse.OptionParser()
    for key in keys:
        parser.add_option("--{0}".format(key),
                          help="run the {0} process".format(key), action="store_true", dest="{0}".format(key),
                          default=False)

    parser.add_option("-a", "--all",
                      help="all the processes", action="store_true", dest="all", default=False)

    options, args = parser.parse_args()
    options = vars(options)

    if options["all"]:
        RuntimeSettings.START_PROCESSES += keys
        return
    for key in keys:
        if options[key]:
            RuntimeSettings.START_PROCESSES.append(key)


def get_process_settings():
    p_settings = {}
    for key in RuntimeSettings.START_PROCESSES:
        p_settings[key] = processes_settings[key]
    return p_settings


# test that everything is running
def validate(exit_on_error=True):
    # mongo
    try:
        client = pymongo.MongoClient(**settings.MONGO, serverSelectionTimeoutMS=1)
        client.server_info()
        client.close()
    except pymongo.errors.ServerSelectionTimeoutError as err:
        if not exit_on_error:
            return False
        print("mongo connection error details:")
        print(err)
        sys.exit(1)

    # rabbit:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(**settings.RABBIT))
        if connection.is_open:
            connection.close()
        else:
            print("RabbitMq connection error.")
            sys.exit(1)
    except Exception as error:
        if not exit_on_error:
            return False
        print("rabbitMq connection error")
        print(error)
        sys.exit(1)
    return True


processes = []


def clean():
    for p in processes:
        try:
            p.kill()
        except:
            pass
    try:
        for file in os.listdir(path("logs")):
            pt = path(path("logs", file))
            if os.path.isfile(pt):
                os.remove(pt)
            else:
                rmtree(pt)
    except:
        pass


def start_process(p_setting):
    kwargs = p_setting["kwargs"]
    strategy = RuntimeSettings.STRATEGIES[p_setting.get("strategy", "p_open_wrapper")]
    t = Thread(target=strategy, kwargs=kwargs)
    t.start()
    return t


def start():
    for setting_name, setting in get_process_settings().items():
        print("Starting {}".format(setting_name))
        start_process(setting)


def wait():
    while not validate(exit_on_error=False):
        sleep(0.0001)


def main():
    parse()
    wait()
    start()


main()
atexit.register(clean)
