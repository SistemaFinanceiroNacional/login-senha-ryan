#!/usr/bin/python3

import sys
import inputIO
import argparse

def main(args, userIO):
    i = 1
    while i < len(args):

        if args[i] == "--folder":
            if i + 1 < len(args):
                if args[i + 1].startswith("--"):
                    userIO.print("Empty Folder")
                    return (1)

                else:
                    userIO.print(f"folder : {args[i + 1]}")

            else:
                userIO.print("Empty Folder")
                return (2)

        elif args[i] == "up":
            userIO.print("up")
            return (0)

        elif args[i] == "down":
            userIO.print("down")
            return (0)

        i += 1


if __name__ == "__main__":
    sys.exit(main(sys.argv, inputIO.inputIO()))
