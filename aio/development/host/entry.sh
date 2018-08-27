dir=$(cd -P -- "$(challenge-framework -- "$0")" && pwd -P)
su root
service docker start
python main.py --docker-host --builder
