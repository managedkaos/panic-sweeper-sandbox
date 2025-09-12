"""
Script to save Varnish panic information and associated core dump files.

This script:

1. Captures panic information from `varnishadm panic.show`
2. Extracts the panic timestamp
3. Finds the matching core dump using `coredumpctl`
4. Saves the panic info, core dump, and dump metadata to files:

   - `HOST-DATE.panic`: Raw panic output
   - `HOST-DATE.dump`: Core dump file
   - `HOST-DATE.info`: Core dump metadata

   Where:

   - `HOST` = hostname
   - `DATE` = panic timestamp in `YYYY-MM-DD-HH-MM-SS` format.

Usage:

    python save-panic-and-coredump.py

Requirements:

   - varnishadm access
   - coredumpctl access
   - Write permissions in current directory
   - Tested with `Python 3.9.19`
"""

import datetime
import socket
import subprocess


def get_panic_date():
    """
    Capture the date from `varnishadm panic.show` and format it for use with coredumpctl.
    """
    try:
        # Run `varnishadm panic.show` and capture output
        panic_output = subprocess.check_output(["varnishadm", "panic.show"], text=True)

        # Extract the date line from the output
        for line in panic_output.splitlines():
            if line.startswith("Panic at:"):
                # Parse the date from the panic log
                panic_date_str = line.split("Panic at:")[1].strip()
                panic_date = datetime.datetime.strptime(
                    panic_date_str, "%a, %d %b %Y %H:%M:%S %Z"
                )
                return panic_date, panic_output
    except subprocess.CalledProcessError as e:
        print("Error running varnishadm panic.show:", e)
    except ValueError as e:
        print("Error parsing panic date format:", e)
    except IndexError as e:
        print("Error extracting panic date from output:", e)

    return None, None


def write_panic_to_file(hostname, date, panic_output):
    """
    Write the panic output to a file named `HOST-DATE.panic`.
    """
    filename = f"{hostname}-{date}.panic"
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(panic_output)
        print(f"Panic output written to {filename}")
    except PermissionError as e:
        print(f"Permission denied when writing to {filename}: {e}")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")


def find_core_dump(panic_date, hostname, date):
    """
    Use `coredumpctl dump` with `--since` and `--until` filters to locate the core dump,
    write it to a file named `HOST-DATE.dump`, and capture the output in `HOST-DATE.info`.
    """
    try:
        # Calculate the time range for matching the core dump
        since_date = panic_date - datetime.timedelta(seconds=1)
        until_date = panic_date + datetime.timedelta(seconds=1)

        # Format dates for `coredumpctl`
        since_str = since_date.strftime("%Y-%m-%d %H:%M:%S")
        until_str = until_date.strftime("%Y-%m-%d %H:%M:%S")

        # File names for dump and diagnostic output
        dump_filename = f"{hostname}-{date}.dump"
        diagnostics_filename = f"{hostname}-{date}.info"

        # Run `coredumpctl dump` to capture the core dump
        command = [
            "coredumpctl",
            "dump",
            "--since",
            since_str,
            "--until",
            until_str,
            "/usr/sbin/varnishd",
            "--output",
            dump_filename,
        ]
        print("Running command:", " ".join(command))
        result = subprocess.check_output(command, text=True)
        print(f"Core dump written to {dump_filename}")

        # Write the diagnostic output to a text file
        with open(diagnostics_filename, "w", encoding="utf-8") as file:
            file.write(result)
        print(f"Diagnostic output written to {diagnostics_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error running coredumpctl dump: {e}")
    except PermissionError as e:
        print(f"Permission error when writing files: {e}")
    except IOError as e:
        print(f"File I/O error processing core dump: {e}")


def main():
    """
    Main function to capture panic information and core dump files.
    """
    # Get the hostname of the system
    hostname = socket.gethostname()

    # Step 1: Get the panic date and output
    panic_date, panic_output = get_panic_date()
    if not panic_date or not panic_output:
        print("No panic date found or unable to retrieve panic output. Exiting.")
        return

    # Format the date for file naming
    formatted_date = panic_date.strftime("%Y-%m-%d-%H-%M-%S")

    # Step 2: Write panic output to file
    write_panic_to_file(hostname, formatted_date, panic_output)

    # Step 3: Find and process the core dump
    find_core_dump(panic_date, hostname, formatted_date)


if __name__ == "__main__":
    main()
