import subprocess
from vcore.configuration.conf_loader import Settings
from vcore.tasks.tasks_importer import TASKS
import atexit

PROCESSES = []

for i, task in enumerate(TASKS):
    strategy = subprocess.Popen
    if i == len(TASKS) - 1:
        strategy = subprocess.call
    print("starting", task)
    cmd = "celery -A {0}  worker --loglevel={1}".format(task, Settings.settings.CELERY.loglevel)
    strategy(cmd.split(" "))


def clean_up():
    for p in PROCESSES:
        p.terminate()


atexit.register(clean_up)
