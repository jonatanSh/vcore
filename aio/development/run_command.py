import sys
import subprocess

cmd = "docker exec -ti web-dev python main.py {0}".format(" ".join(sys.argv[1:]))
print("Executing {0}".format(cmd))
p = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate()

if p.poll() != 0:
    print("Error make sure the server is running using python manage.py runserver")
else:
    print(stdout.decode("utf-8"))
