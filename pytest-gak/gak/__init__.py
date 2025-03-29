import sys
from typing import List

from pytest import console_main


def parse_args(raw_args: List[str] = sys.argv[1:]) -> List[str]:
    """
    Given arguments for pytest, ensure that -s or --capture=no is set.

    This function is not entirely robust, as it doesn't implement full arguments
    parsing as in pytest. If an option is passed "-s" or "--capture=no" as a value,
    this will fail to add the appropriate flag. But those cases should be very
    rare, and a full options parse is difficult.
    """

    args: List[str] = list()

    has_no_capture_flag = False
    for i, arg in enumerate(raw_args):
        if arg == "--capture=no" or arg == "-s":
            has_no_capture_flag = True
            args += raw_args[i:]
            break

        if arg.startswith("--capture="):
            # Drop the flag, since we're going to override it later
            continue

        args.append(arg)

    if not has_no_capture_flag:
        args.insert(0, "--capture=no")

    return args


def main() -> int:
    """
    A command line entry point that calls pytest with --capture=no set.
    """

    args = parse_args()
    # sys.argv[0] is typically the command that was run
    args.insert(0, "pytest")

    # Patch sys.argv so the pytest entry point picks it up
    sys.argv = args

    # Call the standard pytest entry point with modified args
    return console_main()


if __name__ == "__main__":
    sys.exit(main())
