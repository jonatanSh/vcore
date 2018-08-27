import os
import subprocess
import sys

base_dir = os.path.dirname(os.path.dirname(os.getcwd()))

cmd = "python3 main.py --web --docker-host --indexer --runner --builder".split(" ")
cmd += sys.argv[1:]
subprocess.Popen(["docker-compose", "up"])

subprocess.call(cmd, cwd=base_dir)
