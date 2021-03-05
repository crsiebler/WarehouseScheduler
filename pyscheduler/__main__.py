import os
import sys
import getopt
import logging
from .parser import parse


def usage():
    """Help documentation"""
    print(
        f"\nusage: routes_finder [-v] [-h] [--verbose] [--help] "
        f"[--input=<Input-File>] [--output=<Output-File>] "
        f"\nOptions:\n"
        f"\t-v, --verbose\t\tVerbose\n"
        f"\t-h, --help\t\tHelp\n"
        f"\t--input\t\t\tFilename\n"
        f"\t--output\t\tFilename\n"
        f"\nArguments:\n"
        f"\tInput-File: Text file containing the origin & destination input (Default: tests/input/input1.txt).\n"
        f"\tOutput-File: Filename and path where to output the results (Default: tests/output/output1.txt).\n"
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
                "output=",
                "locations=",
                "trips=",
                "results=",
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    # Define input arguments and initialize default values.
    input_file = "tests/input/input1.txt"
    output_file = "tests/output/output1.txt"

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
        elif opt == "--output":
            output_file = arg

    parse(
        input_file,
        output_file,
    )


if __name__ == "__main__":
    main()
