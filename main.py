"""
The main function for panic-sweeper application.
"""

import argparse
import os
import sys

from clean_panic_and_coredump import clean_panic_and_coredump

from save_panic_and_coredump import save_panic_and_coredump


def run_save_panic_and_coredump():
    """
    Run the panic sweeper functionality using the library.
    """
    print("Running panic sweeper...")
    hostname = os.environ.get("HOST", "hostname-not-specified")
    print(f"Hostname: {hostname}")

    result = save_panic_and_coredump()

    if result["no_panic"]:
        print("✅ Child has not panicked or panic has been cleared.")
        return True

    if result["success"]:
        print("✅ Panic sweep completed successfully!")

        if result["panic_file"]:
            print(f"- Panic file: {result['panic_file']}")

        if result["dump_file"]:
            print(f"- Dump file: {result['dump_file']}")

        if result["info_file"]:
            print(f"- Info file: {result['info_file']}")

        print("\nSweep operation complete.")
        return True

    print(f"❌ Error: {result['error']}")
    print("\nSweep operation encountered an error.")
    return False


def run_upload_panic_and_coredump():
    """
    Placeholder function for uploading panic and core dump files.
    """
    print("Upload functionality not yet implemented.")
    print("This function will upload panic and core dump files to a remote location.")
    return False


def run_clean_panic_and_coredump():
    """
    Run the panic cleaner functionality using the library.
    """
    print("Running panic cleaner...")
    hostname = os.environ.get("HOST", "hostname-not-specified")
    print(f"Hostname: {hostname}")

    result = clean_panic_and_coredump()

    if result["no_panic"]:
        print("✅ Child has not panicked or panic has been cleared.")
        return True

    if result["success"]:
        print("✅ Clean sweep completed successfully!")

        if result["panic_cleared"]:
            print("- Panic cleared from varnishadm")

        if result["files_removed"]["panic_files"]:
            n = len(result["files_removed"]["panic_files"])
            label = "file" if n == 1 else "files"
            print(f"- Removed {n} panic {label}")

        if result["files_removed"]["dump_files"]:
            n = len(result["files_removed"]["dump_files"])
            label = "file" if n == 1 else "files"
            print(f"- Removed {n} dump {label}")

        if result["files_removed"]["info_files"]:
            n = len(result["files_removed"]["info_files"])
            label = "file" if n == 1 else "files"
            print(f"- Removed {n} info {label}")

        print("\nSweep operation complete.")
        return True

    print(f"❌ Error: {result['error']}")
    print("\nSweep operation encountered an error.")
    return False


def main():
    """
    Main entry point for panic-sweeper application.
    Uses argparse to handle command-line arguments and subcommands.
    """
    parser = argparse.ArgumentParser(
        description="Panic-sweeper: Collect and process panic files and core dumps from Varnish servers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Available commands", metavar="COMMAND"
    )

    # Save command
    subparsers.add_parser(
        "save", help="Save panic information and associated core dump files"
    )

    # Upload command (placeholder)
    subparsers.add_parser(
        "upload", help="Upload panic and core dump files to a remote location"
    )

    # Clean command
    subparsers.add_parser("clean", help="Clean up old panic and core dump files")

    # Parse arguments
    args = parser.parse_args()

    # If no command provided, show help
    if args.command is None:
        parser.print_help()
        sys.exit(0)

    # Execute the appropriate command
    success = False

    if args.command == "save":
        success = run_save_panic_and_coredump()

    elif args.command == "upload":
        success = run_upload_panic_and_coredump()

    elif args.command == "clean":
        success = run_clean_panic_and_coredump()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
