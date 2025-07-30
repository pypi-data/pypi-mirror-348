import sys
import importlib

import arkalos.core.logger.log as Log
from arkalos.core.bootstrap import bootstrap

RESET = '\033[0m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'

ENABLED_COMMANDS = {
    'init': 'Init the Arkalos starter project with the base folder structure and configuration.',
    'serve': 'Start Arkalos HTTP API Server.',
    'make:mw': 'Generate a new middleware class' 
}

def show_help():
    print()
    print(BLUE + 'Arkalos')
    print('The Python Framework for AI & Data Artisans')
    print('Copyright (c) 2025 Mev-Rael')
    print('v0.6.0 (Beta 6)')
    print()
    print("Available commands:" + RESET)
    for command in ENABLED_COMMANDS:
        print(f"  {GREEN}{command}{RESET} - {YELLOW}{ENABLED_COMMANDS[command]}{RESET}")
    print()
    print(f"{BLUE}Use '{GREEN}uv run arkalos <command>{BLUE}' to run a command.{RESET}")
    print()

def run_command(command):
    if command in ENABLED_COMMANDS:
        try:
            module = importlib.import_module(f'arkalos.cli.{command.replace(':', '_')}')
            module.run()
        except ModuleNotFoundError:
            print()
            print(f"Command '{command}' is not implemented properly.")
            print()
    else:
        print()
        print(f"Command '{command}' is not available. Please use a valid command.")
        print()

def main():
    try:
        if len(sys.argv) < 2:
            show_help()
            return
        
        command = sys.argv[1]
        if command != 'init':
            bootstrap().register()
        Log.logger()
        
        run_command(command)
    except Exception as e:
        Log.exception(e)



if __name__ == "__main__":
    main()
