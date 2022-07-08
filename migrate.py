#!/usr/bin/python3

import sys

def main(args):
    i = 1
    while i < len(args):

        if args[i] == "--folder":
            if i+1 < len(args):
                if args[i+1].startswith("--"):
                    print("Empty Folder")
                    return(1)

                else:
                    print(f"folder : {args[i + 1]}")

            else:
                print("Empty Folder")
                return(2)

        elif args[i] == "up":
            print("up")
            return(0)

        elif args[i] == "down":
            print("down")
            return(0)

        i += 1





if __name__ == "__main__":
    sys.exit(main(sys.argv))
