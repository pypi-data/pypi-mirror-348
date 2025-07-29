#!/usr/bin/env python3
from flask import Flask, request, send_file, jsonify
import subprocess, os
from pathlib import Path

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def handle_download():
    d = request.get_json(force=True)
    url  = d.get("url")
    acc  = d.get("mullvad_account")
    res  = d.get("resolution")
    ext  = d.get("extension")

    if not url or not acc:
        return jsonify(error="url and mullvad_account required"), 400

    cmd = ["python3", "-m", "ytp_dl.mdl", url, acc]
    if res: cmd += ["--resolution", res]
    if ext: cmd += ["--extension",  ext]

    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode:
        return jsonify(error="Download failed", output=proc.stdout), 500

    fname = next((l.split("DOWNLOADED_FILE:")[1].strip()
                  for l in proc.stdout.splitlines()
                  if l.startswith("DOWNLOADED_FILE:")), None)

    if fname and Path(fname).exists():
        return send_file(fname, as_attachment=True, download_name=Path(fname).name)
    return jsonify(error="No downloaded file found", output=proc.stdout), 404

def main():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
