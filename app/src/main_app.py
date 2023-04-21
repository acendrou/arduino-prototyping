import signal

from core.misc.app import App

# Analysis GUI
# C3 Command, Control, Console - pretty console output & command and control & see (c)

app = App(multiprocessing=False)


def main_app():
    global app
    app.run()


def terminate_gracefully(signum, frame):
    global app
    print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    if signum == signal.SIGINT:
        print("SIGINT catched")
    if signum == signal.SIGTERM:
        print("SIGTERM catched")
    del app


signal.signal(signal.SIGTERM, terminate_gracefully)
signal.signal(signal.SIGINT, terminate_gracefully)

if __name__ == '__main__':
    main_app()
