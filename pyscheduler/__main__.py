import os
from pyscheduler.scheduler import InvalidScheduleException
import sys
import getopt
import logging
from .parser import parse


def usage():
    """Help documentation"""
    print(
        f"\nusage: routes_finder [-v] [-h] [--verbose] [--help] "
        f"[--input=<Input-File>]"
        f"\nOptions:\n"
        f"\t-v, --verbose\t\tVerbose\n"
        f"\t-h, --help\t\tHelp\n"
        f"\t--input\t\t\tFilename\n"
        f"\nArguments:\n"
        f"\tInput-File: Text file containing the origin & destination input (Default: tests/input/sameday.txt).\n"
    )


def main():
    """"""
    # Check the user CLI input matches correct syntax
    try:
        # Specify the valid CLI options/arguments
        opts, _ = getopt.getopt(
            sys.argv[1:],
            "hv",
            [
                "help",
                "verbose",
                "input=",
            ],
        )
    except getopt.GetoptError as err:
        logging.error(str(err))
        usage()
        sys.exit(2)

    # Define input arguments and initialize default values.
    input_file = "tests/input/sameday.txt"

    # Loop through all the User CLI options/arguments
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-v", "--verbose"):
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
        elif opt == "--input":
            input_file = arg

            if not os.path.exists(input_file):
                sys.exit("Could not find input file")

    try:
        print(parse(input_file))
    except InvalidScheduleException:
        # Invalid schedule given
        sys.exit(2)


if __name__ == "__main__":
    main()
