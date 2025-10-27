"""Simple CLI for running the app, web UI or tests."""
import argparse
import subprocess
import sys
from pathlib import Path


def run_app():
    # run the local camera authentication
    import app
    app.run_auth()


def run_web():
    # start the Flask web UI
    import webui
    webui.run_server()


def run_tests():
    # run unit tests
    subprocess.check_call([sys.executable, '-m', 'unittest', 'discover', '-v'])


def main():
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=['run', 'web', 'test'], help='run|web|test')
    args = p.parse_args()

    if args.command == 'run':
        run_app()
    elif args.command == 'web':
        run_web()
    elif args.command == 'test':
        run_tests()


if __name__ == '__main__':
    main()
