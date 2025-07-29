#!/usr/bin/env python3
import subprocess
import sys
import os
import time
import shutil
import argparse


def run_command(cmd, check=True):
    try:
        result = subprocess.run(
            cmd, shell=True, check=check,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}\nError: {e.output}")
        raise


def ensure_venv_with_packages(venv_path):
    if not os.path.exists(f"{venv_path}/bin/yt-dlp") or not os.path.exists(f"{venv_path}/bin/flask"):
        print("Creating virtual environment and installing required packages...")
        run_command(f"python3 -m venv {venv_path}")
        run_command(f"{venv_path}/bin/pip install --upgrade pip yt-dlp flask")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="YouTube URL")
    parser.add_argument("mullvad_account", help="Mullvad account number")
    parser.add_argument("--resolution", help="Desired resolution (e.g., 1080)", default=None)
    parser.add_argument("--extension", help="Desired file extension (e.g., mp4, mp3)", default=None)
    args = parser.parse_args()


    venv_path = "/opt/yt-dlp-mullvad/venv"
    ensure_venv_with_packages(venv_path)


    print("Checking for Mullvad CLI...")
    if not shutil.which("mullvad"):
        print("Mullvad CLI not found.")
        sys.exit(1)


    print("Logging into Mullvad...")
    run_command(f"mullvad account login {args.mullvad_account}")


    print("Connecting to Mullvad VPN...")
    run_command("mullvad connect")
    time.sleep(10)


    print(f"Downloading: {args.url}")


    audio_extensions = ["mp3", "m4a", "aac", "wav", "flac", "opus", "ogg"]
    if args.extension and args.extension in audio_extensions:
        ytdlp_cmd = (
            f"{venv_path}/bin/yt-dlp -x --audio-format {args.extension} "
            f"--embed-metadata "
            f"--output '/root/%(title)s.%(ext)s' "
            f"--user-agent 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' {args.url}"
        )
    else:
        if args.resolution:
            format_filter = f"bestvideo[height<={args.resolution}]+bestaudio/best[height<={args.resolution}]"
        else:
            format_filter = "bestvideo+bestaudio"
        merge_extension = args.extension if args.extension else "mp4"
        ytdlp_cmd = (
            f"{venv_path}/bin/yt-dlp -f '{format_filter}' --merge-output-format {merge_extension} "
            f"--embed-thumbnail --embed-metadata "
            f"--output '/root/%(title)s.%(ext)s' "
            f"--user-agent 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' {args.url}"
        )


    try:
        output = run_command(ytdlp_cmd)
        filename = None
        for line in output.splitlines():
            if line.startswith("[download]"):
                if "Destination:" in line:
                    filename = line.split("Destination: ")[1].strip()
                elif "has already been downloaded" in line:
                    start = line.find("] ") + 2
                    end = line.find(" has already been downloaded")
                    filename = line[start:end].strip()
                    if filename.startswith("'") and filename.endswith("'"):
                        filename = filename[1:-1]
                break
        if filename and os.path.exists(filename):
            print(f"DOWNLOADED_FILE:{filename}")
        else:
            print("Download failed: File not found")
    except subprocess.CalledProcessError as e:
        print(f"yt-dlp failed with error: {e.output}")


    print("Disconnecting VPN...")
    run_command("mullvad disconnect")


if __name__ == "__main__":
    main()
