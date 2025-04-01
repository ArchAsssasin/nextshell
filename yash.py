import os
import subprocess
import getpass
import readline
from colorama import Fore, Style, init
import platform

init()

USER = getpass.getuser()
HOSTNAME = os.uname().nodename

def get_distribution_name():
    try:
        with open('/etc/os-release') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('PRETTY_NAME'):
                    return line.split('=')[1].strip().strip('"')
    except Exception as e:
        return "Unknown Distribution"

DISTRO_NAME = get_distribution_name()

readline.parse_and_bind('tab: complete')
readline.set_completer_delims(' \t\n')

aliases = {}

internal_commands = ['cd', 'exit', 'pwd', 'echo', 'export', 'unset']

HOME = os.path.expanduser('~')

def yash_prompt():
    """Return the custom YaSH prompt"""
    home_dir = os.path.expanduser("~")
    cwd = os.getcwd().replace(home_dir, "~", 1)
    return f"{Fore.BLUE}{USER}{Style.RESET_ALL}@{Fore.GREEN}{HOSTNAME}{Style.RESET_ALL} | {Fore.WHITE}{cwd}{Style.RESET_ALL}\n==> "

def execute_command(command):
    """Execute commands and show output"""
    global aliases

    if command.split()[0] in aliases:
        command = aliases[command.split()[0]] + ' ' + ' '.join(command.split()[1:])

    if command.startswith("cd "):
        try:
            target_dir = command.split(" ", 1)[1] if len(command.split()) > 1 else HOME
            os.chdir(target_dir)
        except Exception as e:
            print(f"Error: {e}")
    elif command == "exit":
        print("Exiting YaSH...")
        exit(0)
    elif command == "pwd":
        print(os.getcwd())
    elif command.startswith("echo "):
        print(command[5:])
    elif command.startswith("export "):
        try:
            var = command.split('=', 1)[0].split()[1]
            value = command.split('=', 1)[1]
            os.environ[var] = value
        except Exception as e:
            print(f"Error: {e}")
    elif command.startswith("unset "):
        try:
            var = command.split()[1]
            if var in os.environ:
                del os.environ[var]
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            subprocess.run(command, shell=True)
        except Exception as e:
            print(f"Error: {e}")

def add_alias(alias, command):
    aliases[alias] = command

def handle_keyboard_shortcuts(command):
    if command == '\\x03':  # Ctrl+C
        return True
    elif command == '\\x04':  # Ctrl+D
        print('Exiting YaSH...')
        exit(0)
    elif command == '\\x15':  # Ctrl+U
        print('Cursor moved to the beginning and content cleared.')
        return ''
    elif command == '\\x0b':  # Ctrl+K
        print('Cursor moved to the end and content cleared.')
        return ''
    elif command == '\\x0c':  # Ctrl+L
        os.system('clear')
        return ''
    return command

def complete_command(text, state):
    """A simple function for command completion"""
    options = ['cd', 'exit', 'pwd', 'echo', 'export', 'unset']
    return [option for option in options if option.startswith(text)][state]

readline.set_completer(complete_command)

if __name__ == "__main__":
    os.environ["SHELL"] = "/usr/bin/yash"  # Write the full path of YaSH here

    print(f"YaSH Shell - Running on {DISTRO_NAME} operating system.")
    while True:
        try:
            command = input(yash_prompt())
            command = handle_keyboard_shortcuts(command)
            execute_command(command)
        except KeyboardInterrupt:
            print("\nType 'exit' to quit.")
