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
import sys


def get_panic_date():
    """
    Capture the date from `varnishadm panic.show` and format it for use with coredumpctl.
    """
    try:
        # Run `varnishadm panic.show` and capture output
        panic_output = subprocess.check_output(
            ["sudo", "varnishadm", "panic.show"], text=True
        )

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

    Args:
        hostname (str): Hostname for file naming
        date (str): Formatted date string for file naming
        panic_output (str): Panic output content to write

    Returns:
        str: Filename if successful, None if failed
    """
    filename = f"{hostname}-{date}.panic"
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(panic_output)
        print(f"Panic output written to {filename}")
        return filename
    except PermissionError as e:
        print(f"Permission denied when writing to {filename}: {e}")
        return None
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")
        return None


def find_core_dump(panic_date, hostname, date):
    """
    Use `coredumpctl dump` with `--since` and `--until` filters to locate the core dump,
    write it to a file named `HOST-DATE.dump`, and capture the output in `HOST-DATE.info`.

    Args:
        panic_date (datetime): The panic date to search around
        hostname (str): Hostname for file naming
        date (str): Formatted date string for file naming

    Returns:
        dict: Dictionary with 'dump_file' and 'info_file' keys if successful, None if failed
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

        return {"dump_file": dump_filename, "info_file": diagnostics_filename}
    except subprocess.CalledProcessError as e:
        print(f"Error running coredumpctl dump: {e}")
        return None
    except PermissionError as e:
        print(f"Permission error when writing files: {e}")
        return None
    except IOError as e:
        print(f"File I/O error processing core dump: {e}")
        return None


def save_panic_and_coredump(hostname=None):
    """
    Main function to capture panic information and core dump files.

    Args:
        hostname (str, optional): Hostname to use for file naming.
                                 If None, uses socket.gethostname()

    Returns:
        dict: Dictionary containing the results with keys:
              - 'success': bool indicating if operation succeeded
              - 'panic_file': str path to panic file if created
              - 'dump_file': str path to dump file if created
              - 'info_file': str path to info file if created
              - 'error': str error message if operation failed
    """
    result = {
        "success": False,
        "panic_file": None,
        "dump_file": None,
        "info_file": None,
        "error": None,
    }

    try:
        # Get the hostname of the system
        if hostname is None:
            hostname = socket.gethostname()

        # Step 1: Get the panic date and output
        panic_date, panic_output = get_panic_date()
        if not panic_date or not panic_output:
            result["error"] = "No panic date found or unable to retrieve panic output"
            return result

        # Format the date for file naming
        formatted_date = panic_date.strftime("%Y-%m-%d-%H-%M-%S")

        # Step 2: Write panic output to file
        panic_file = write_panic_to_file(hostname, formatted_date, panic_output)
        if panic_file:
            result["panic_file"] = panic_file

        # Step 3: Find and process the core dump
        dump_files = find_core_dump(panic_date, hostname, formatted_date)
        if dump_files:
            result["dump_file"] = dump_files.get("dump_file")
            result["info_file"] = dump_files.get("info_file")

        result["success"] = True
        return result

    except Exception as e:
        result["error"] = str(e)
        return result


def main():
    """
    Command-line interface for the panic sweeper library.
    """
    result = save_panic_and_coredump()

    if result["success"]:
        print("Panic and core dump saved successfully!")
        if result["panic_file"]:
            print(f"Panic file: {result['panic_file']}")
        if result["dump_file"]:
            print(f"Dump file: {result['dump_file']}")
        if result["info_file"]:
            print(f"Info file: {result['info_file']}")
    else:
        print(f"Error: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
