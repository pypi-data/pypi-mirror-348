#!/usr/bin/env python3
import subprocess, sys, os, time, shutil, argparse

def run_command(cmd, check=True):
    try:
        res = subprocess.run(
            cmd, shell=True, check=check,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Command failed:", cmd, "\n", e.output)
        raise

def ensure_venv_with_packages(venv):
    if not (os.path.exists(f"{venv}/bin/yt-dlp")
            and os.path.exists(f"{venv}/bin/flask")):
        print("Creating venv and installing packages…")
        run_command(f"python3 -m venv {venv}")
        run_command(f"{venv}/bin/pip install --upgrade pip yt-dlp flask")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("mullvad_account")
    p.add_argument("--resolution")
    p.add_argument("--extension")
    a = p.parse_args()

    venv = "/opt/yt-dlp-mullvad/venv"
    ensure_venv_with_packages(venv)

    if not shutil.which("mullvad"):
        print("Mullvad CLI not found"); sys.exit(1)

    run_command(f"mullvad account login {a.mullvad_account}")
    run_command("mullvad connect"); time.sleep(10)

    audio = {"mp3","m4a","aac","wav","flac","opus","ogg"}
    if a.extension in audio:
        ytdlp = (f"{venv}/bin/yt-dlp -x --audio-format {a.extension} "
                 f"--embed-metadata --output '/root/%(title)s.%(ext)s' "
                 f"--user-agent 'Mozilla/5.0' {a.url}")
    else:
        fmt = (f"bestvideo[height<={a.resolution}]+bestaudio/"
               f"best[height<={a.resolution}]") if a.resolution else "bestvideo+bestaudio"
        merge = a.extension or "mp4"
        ytdlp = (f"{venv}/bin/yt-dlp -f '{fmt}' --merge-output-format {merge} "
                 f"--embed-thumbnail --embed-metadata "
                 f"--output '/root/%(title)s.%(ext)s' "
                 f"--user-agent 'Mozilla/5.0' {a.url}")

    out = run_command(ytdlp)
    fname = next((l.split("Destination: ")[1].strip()
                  for l in out.splitlines() if "Destination:" in l), None)
    if fname and os.path.exists(fname):
        print(f"DOWNLOADED_FILE:{fname}")
    else:
        print("Download failed: file not found")

    run_command("mullvad disconnect")

if __name__ == "__main__":
    main()
