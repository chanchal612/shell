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

def write_output(text, stdout_redirect_file, stdout_mode):
    if stdout_redirect_file:
        with open(stdout_redirect_file, stdout_mode) as out:
            out.write(text + "\n")
    else:
        print(text)



def main():
    
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()
        parts=[]
        current =""
        inside_singles = False
        inside_doubles = False

        i = 0
        while i < len(command):
            char = command[i]
            if char == "'":
                if inside_doubles:
                    current += char
                    i += 1
                    continue
                else:
                    inside_singles = not inside_singles
                    i += 1
                    continue
            if char == '"':
                if inside_singles:
                    current += char
                    i += 1
                    continue
                else:
                    inside_doubles = not inside_doubles
                    i += 1
                    continue
            if char == " " and not inside_singles and not inside_doubles:
                if current:
                    parts.append(current)
                    current = ""
                i += 1
                continue
            if char == "\\" and not inside_singles and not inside_doubles:
                if i + 1 < len(command):
                    current += command[i + 1]
                    i += 2
                    continue
                else:
                    current += char
                    i += 1
                    continue
            if char == "\\" and inside_doubles:
                if i + 1 < len(command):
                    current += command[i + 1]
                    i += 2
                    continue
                else:
                    current += char
                    i += 1
                    continue

            else:
                current += char
            i += 1
        if current:
            parts.append(current)

        
        if not parts:
            continue
        
        i = 0
        stdout_redirect_file =""
        stderr_redirect_file =""
        stdout_mode = None

        while i < len(parts):
            if parts[i] == ">" or parts[i] == "1>":
                if i + 1 < len(parts):
                    stdout_redirect_file = parts[i + 1]
                    parts = parts[:i]
                    stdout_mode = "w"
                    break
                else:
                    print("Syntax error: expected filename after '>'")
                    break
            elif parts[i] == "2>":
                if i + 1 < len(parts):
                    stderr_redirect_file = parts[i + 1]
                    parts = parts[:i]
                    stdout_mode = "w"
                    break
                else:
                    print("Syntax error: expected filename after '2>'")
                    break
            elif parts[i] == ">>" or parts[i] == "1>>":
                if i + 1 < len(parts):
                    stdout_redirect_file = parts[i + 1]
                    parts = parts[:i]
                    stdout_mode = "a"
                    break
            elif parts[i] == "2>>":
                if i + 1 < len(parts):
                    stderr_redirect_file = parts[i + 1]
                    parts = parts[:i]
                    stdout_mode = "a"
                    break
                else:
                    print("Syntax error: expected filename after '2>>'")
                    break
            i += 1
        
        if parts[0] == "exit":
            break
        elif parts[0] == "type":
            if parts[1] in ["echo", "exit", "type", "pwd"]:
                print(f"{parts[1]} is a shell builtin")
                continue
            else:

                path = path_command(parts[1])
                
                if path:
                    print(f"{parts[1]} is {path}")
                else:
                    print(f"{" ".join(parts[1:])}: not found")
               
        elif parts[0] == "echo":
            if stderr_redirect_file:
                with open(stderr_redirect_file, stdout_mode) as err:
                    pass
            write_output(" ".join(parts[1:]), stdout_redirect_file, stdout_mode)

        elif parts[0] == "pwd":
            print(os.getcwd())

        elif parts[0] == "cd":

            if os.path.isdir(parts[1]):
                os.chdir(parts[1])

            elif parts[1] == "~":
                home = os.getenv("HOME")
                if home:
                    os.chdir(home)
                else:
                    print("cd: HOME environment variable is not set")

            else:
                print(f"cd: {parts[1]}: No such file or directory")



        else:
            path = path_command(parts[0])
            if path:
                if stdout_redirect_file:
                    with open(stdout_redirect_file, stdout_mode) as out:
                        subprocess.run(parts,executable=path,stdout=out)
                elif stderr_redirect_file:
                    with open(stderr_redirect_file, stdout_mode) as err:
                        subprocess.run(parts,executable=path,stderr=err)
                else:
                    subprocess.run(parts,executable=path)
            else:
                print(f"{command}: command not found")

            
            


if __name__ == "__main__":
    main()  