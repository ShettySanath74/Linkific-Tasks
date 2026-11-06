
import os
import paramiko
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DOWNLOAD_DIR = BASE_DIR / "data" / "files" / "sftp"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def collect_sftp_file():

    host = os.getenv("SFTP_HOST")
    username = os.getenv("SFTP_USERNAME")
    password = os.getenv("SFTP_PASSWORD")

    remote_file = os.getenv(
        "SFTP_REMOTE_FILE",
        "/upload/sales.csv"
    )

    if not all([host, username, password]):
        raise ValueError(
            "Set SFTP_HOST, SFTP_USERNAME and SFTP_PASSWORD."
        )

    transport = None
    sftp = None

    try:
        print("Connecting to SFTP server...")

        transport = paramiko.Transport((host, 22))

        transport.connect(
            username=username,
            password=password
        )

        sftp = paramiko.SFTPClient.from_transport(transport)

        print("SFTP connection successful!")

        print("\nRemote files:")
        print(sftp.listdir("/"))

        filename = Path(remote_file).name
        local_file = DOWNLOAD_DIR / filename

        sftp.get(remote_file, str(local_file))

        print("\nFile downloaded successfully!")
        print("Saved to:", local_file)

    except Exception as error:
        print("SFTP collection failed:", error)

    finally:
        if sftp:
            sftp.close()

        if transport:
            transport.close()


if __name__ == "__main__":
    collect_sftp_file()
