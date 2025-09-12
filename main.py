"""
The main function
"""

import socket
import sys

from save_panic_and_coredump import find_core_dump, get_panic_date, write_panic_to_file


def custom_function(function_input):
    """
    Update or replace this function as needed.
    """
    return f"Custom function output: {function_input}"


if __name__ == "__main__":
    # Set the input to be sys.argv[1] if it exists
    # otherwise set it to a default value
    if len(sys.argv) < 2:
        sys.argv.append("default_value")

    hostname = socket.gethostname()
    print(custom_function(sys.argv[1]))

    # Step 1: Get the panic date and output
    panic_date, panic_output = get_panic_date()
    if not panic_date or not panic_output:
        print("No panic date found or unable to retrieve panic output. Exiting.")
        sys.exit(0)

    # Format the date for file naming
    formatted_date = panic_date.strftime("%Y-%m-%d-%H-%M-%S")

    # Step 2: Write panic output to file
    write_panic_to_file(hostname, formatted_date, panic_output)

    # Step 3: Find and process the core dump
    find_core_dump(panic_date, hostname, formatted_date)
