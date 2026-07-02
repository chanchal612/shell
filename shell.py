from imaplib import Commands
from importlib.resources import path
import sys
import os
import subprocess


def find_command(command):

    paths = os.environ.get("PATH", "").split(os.pathsep)

    for path in paths:

        full_path = os.path.join(path, command)

        if os.path.isfile(full_path)and os.access(full_path, os.X_OK):
            return full_path

        if os.path.isfile(full_path + ".exe") and os.access(full_path + ".exe", os.X_OK):
            return full_path + ".exe"
        
    return None


def main():
    while True:
        sys.stdout.write("$ ")
        
        command = input()
 
        path = find_command(command)

        if path:
            subprocess.run([path] + command[1:])
        else:
            print(f"{command}: command not found")

        command = command.split()

        if command[0] == "echo":
            print(" ".join(command[1:]))

        elif command[0] == "exit":
            break
        
        elif command[0] == "type":
            if command[1] == "echo":

                print(f"{command[1]} is a shell builtin")
            
            elif command[1] == "exit":
                print(f"{command[1]} is a shell builtin")
            
            elif command[1] == "type":
                print(f"{command[1]} is a shell builtin")
            
            else:
                path = find_command(command[1])
                
                if path:
                    print(f"{command[1]} is {path}")
                
                else:
                    path = find_command(command[0])

                    if path:
                        subprocess.run([path] + command[1:])
                    else:
                        print(f"{command[0]}: command not found")

        else:
            print(f"{ " ".join(command[0:])}: command not found")

        
        


if __name__ == "__main__":
    main()