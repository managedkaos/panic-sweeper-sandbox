"""
The main function for panic-sweeper application.
"""

import socket
import sys

from save_panic_and_coredump import save_panic_and_coredump


def custom_function(function_input):
    """
    Update or replace this function as needed.
    """
    return f"Custom function output: {function_input}"


def run_panic_sweeper():
    """
    Run the panic sweeper functionality using the library.
    """
    print("Running panic sweeper...")
    result = save_panic_and_coredump()

    if result["success"]:
        print("✅ Panic and core dump saved successfully!")
        if result["panic_file"]:
            print(f"📄 Panic file: {result['panic_file']}")
        if result["dump_file"]:
            print(f"💾 Dump file: {result['dump_file']}")
        if result["info_file"]:
            print(f"ℹ️  Info file: {result['info_file']}")
        return True
    else:
        print(f"❌ Error: {result['error']}")
        return False


if __name__ == "__main__":
    # Set the input to be sys.argv[1] if it exists
    # otherwise set it to a default value
    if len(sys.argv) < 2:
        sys.argv.append("default_value")

    hostname = socket.gethostname()

    # Run the panic sweeper
    print(f"Hostname: {hostname}")
    success = run_panic_sweeper()

    if success:
        print("\n🎉 Panic sweeper completed successfully!")
    else:
        print("\n💥 Panic sweeper encountered an error.")
        sys.exit(1)
