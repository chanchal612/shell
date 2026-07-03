import sys

def main():
    
    while True:
        sys.stdout.write("$ ")
        command = input()

        parts= command.split()
    
        if parts[0] == "exit":
            break
        elif parts[0] == "type":
            if parts[1] in ["echo", "exit", "type"]:
                print(f"{parts[1]} is a shell builtin")
            else:
                print(f"{" ".join(parts[1:])}: not found")
               
        elif parts[0] == "echo":
            print(" ".join(parts[1:]))
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()