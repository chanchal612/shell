import sys
import os
import subprocess

def path_command(command_name):
    paths = os.getenv("PATH", "").split(os.pathsep)

    for path in paths:
        full_path = os.path.join(path, command_name)

        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
        
        if os.path.isfile(full_path + ".exe"):
            return full_path + ".exe"
        
    return None 



def main():
    
    while True:
        sys.stdout.write("$ ")
        command = input()
        parts= command.split()

        if not parts:
            continue

        if parts[0] == "exit":
            break
        elif parts[0] == "type":
            if parts[1] in ["echo", "exit", "type"]:
                print(f"{parts[1]} is a shell builtin")
                continue
            else:

                path = path_command(parts[1])
                
                if path:
                    print(f"{parts[1]} is {path}")
                else:
                    print(f"{" ".join(parts[1:])}: not found")
               
        elif parts[0] == "echo":
            print(" ".join(parts[1:]))


        else:
            path = path_command(parts[0])
            if path:
                subprocess.run(parts, executable=path)
            else:
                print(f"{command}: command not found")

            


if __name__ == "__main__":
    main()  