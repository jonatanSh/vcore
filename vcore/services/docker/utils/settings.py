import os
import logging

MONGO = {
    'host': os.getenv("mongo_host", "localhost"),
    'port': 27017,
}

RABBIT = {
    'host': os.getenv("rabbit_host", "localhost"),
    'port': 5672,
}

DOCKER_HOST = {
    'host': os.getenv("docker_host", "localhost"),
    'server_host': "0.0.0.0",
    'backlog': 100,
    'port': 1111,
}

CHALLENGES = {
    'process_challenges_queue': "process_challenges",
    "challenge_collection": "challenges",
    "ready_challenges_queue": "ready_challenges",
    "db": "challenge_framework",
    "run_challenge_queue": "run_challenge",
}

LOGGING_SETTINGS = {
    # "filename": "/var/log/challenge_framework.log",
    "level": logging.INFO,
}
