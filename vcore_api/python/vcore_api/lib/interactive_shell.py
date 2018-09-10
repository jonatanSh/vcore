import eel
import os

BASE_DIR = os.path.dirname(__file__)


def create_shell(handler):
    @eel.expose
    def handle_input(input):
        return handler(input)

    eel.init(os.path.join(BASE_DIR, 'shell'))
    eel.start('main.html', size=(800, 460))


def stop_shell():
    exit(0)
