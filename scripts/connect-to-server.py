import json
import shutil
import signal
import subprocess
import sys

import boto3


def check_session_manager_plugin():
    if shutil.which("session-manager-plugin") is None:
        print("Error: AWS Session Manager plugin is not installed.")
        print("\nPlease install the AWS Session Manager plugin:")
        print("\nFor macOS (using Homebrew):")
        print("brew install --cask session-manager-plugin")
        print("\nFor Linux (using curl):")
        print(
            "curl 'https://s3.amazonaws.com/session-manager-downloads/plugin/latest/mac/sessionmanager-bundle.zip' -o 'sessionmanager-bundle.zip'"
        )
        print("unzip sessionmanager-bundle.zip")
        print(
            "sudo ./sessionmanager-bundle/install -i /usr/local/sessionmanagerplugin -b /usr/local/bin/session-manager-plugin"
        )
        print("\nFor Windows:")
        print(
            "Download and install from: https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html"
        )
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: python connect-to-server.py <instance-id>")
        sys.exit(1)

    # Check if session-manager-plugin is installed
    check_session_manager_plugin()

    instance_id = sys.argv[1]
    ssm = boto3.client("ssm")

    print(f"## Starting session to instance: {instance_id}")
    print("## Press `CTRL+D` or type `exit` to end the session")

    # Set up signal handling to pass SIGINT (CTRL+C) to the subprocess
    def signal_handler(signum, frame):
        # Pass the signal to the subprocess
        pass

    signal.signal(signal.SIGINT, signal_handler)

    try:
        # Start the SSM session
        response = ssm.start_session(
            Target=instance_id,
            DocumentName="AWS-StartInteractiveCommand",
            Parameters={"command": ["/bin/bash"]},
        )

        # Extract the session details
        session_id = response["SessionId"]
        token_value = response["TokenValue"]
        stream_url = response["StreamUrl"]

        # Start the session using the AWS CLI
        subprocess.run(
            [
                "session-manager-plugin",
                json.dumps(
                    {
                        "SessionId": session_id,
                        "TokenValue": token_value,
                        "StreamUrl": stream_url,
                    }
                ),
                "us-east-1",  # You may want to make this configurable
                "StartSession",
            ]
        )

    except Exception as e:
        print(f"Error connecting to instance {instance_id}: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
