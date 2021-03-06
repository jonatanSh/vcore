try:
    from __init__ import *
except ImportError:
    from .__init__ import *

import subprocess
from vcore.configuration.conf_loader import Settings
from vcore.tasks.tasks_importer import TASKS
import atexit

PROCESSES = []

for i, task in enumerate(TASKS):
    queue = TASKS[task]
    strategy = subprocess.Popen
    if i == len(TASKS) - 1:
        strategy = subprocess.call
    print("starting", task, "startegy", strategy)
    cmd = ["celery", "-A", task, "worker",
           "--loglevel={0}".format(Settings.settings.CELERY.loglevel),
           "--hostname={0}@{1}".format(task, Settings.settings.CELERY.broker),
           "-Q", queue]
    strategy(cmd, cwd=os.path.join(os.getcwd(), "../../"))


def clean_up():
    for p in PROCESSES:
        p.terminate()


atexit.register(clean_up)
