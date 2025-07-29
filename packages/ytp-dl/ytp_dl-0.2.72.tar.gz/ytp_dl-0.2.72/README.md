# ytp-dl

A privacy-focused YouTube downloader built on top of `yt-dlp`, leveraging **Mullvad VPN** for anonymized requests. Supports both CLI and API usage for downloading video or audio with customizable resolution and format.

---

## 📦 Installation

### 1. System Dependencies

Install the required system packages (Debian-based systems):

```bash
sudo apt update && sudo apt install -y python3-venv python3-pip curl ffmpeg
curl -fsSLo /tmp/mullvad.deb https://mullvad.net/download/app/deb/latest/
sudo apt install -y /tmp/mullvad.deb
```

Ensure the Mullvad VPN app is installed and logged in.

---

### 2. Python Package

```bash
pip install ytp-dl
```

---

## ▶️ CLI Usage

Download a video or audio file over a Mullvad VPN tunnel:

```bash
ytp-dl 'https://youtu.be/VIDEO_ID' <MULLVAD_ACCOUNT_NUMBER> --output-dir /path/to/save [--resolution 1080] [--extension mp4]
```

### Arguments

- `YouTube URL` — Required. Video or playlist URL.
- `Mullvad Account Number` — Required. 16-digit Mullvad number (no spaces).
- `--output-dir` — Required. Output directory path.
- `--resolution` — Optional. Video resolution (e.g., 1080, 720).
- `--extension` — Optional. File format (e.g., mp4, mp3).

---

## 🌐 API Usage

Start the Flask API server:

```bash
ytp-dl-api
```

### 🔁 Testing the API with `curl`

#### Download best video (default: mp4)

```bash
curl -X POST "http://<your_droplet_ip>:5000/api/download" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ", "mullvad_account":"<your_mullvad_account_number>"}' \
  -O -J
```

#### Download specific resolution

```bash
curl -X POST "http://<your_droplet_ip>:5000/api/download" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ", "resolution":"720", "mullvad_account":"<your_mullvad_account_number>"}' \
  -O -J
```

#### Download specific extension

```bash
curl -X POST "http://<your_droplet_ip>:5000/api/download" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ", "extension":"mkv", "mullvad_account":"<your_mullvad_account_number>"}' \
  -O -J
```

#### Download audio

```bash
curl -X POST "http://<your_droplet_ip>:5000/api/download" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ", "extension":"mp3", "mullvad_account":"<your_mullvad_account_number>"}' \
  -O -J
```

#### Download with resolution and format

```bash
curl -X POST "http://<your_droplet_ip>:5000/api/download" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ", "resolution":"1080", "extension":"webm", "mullvad_account":"<your_mullvad_account_number>"}' \
  -O -J
```

---

## 🛠️ Optional: systemd Service

Run the API server persistently using `systemd`.

### 1. Create a service file:

```bash
sudo nano /etc/systemd/system/ytp-dl-api.service
```

### 2. Paste:

```ini
[Unit]
Description=Flask API for ytp-dl Mullvad Downloader
After=network.target

[Service]
ExecStart=/usr/local/bin/ytp-dl-api
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```

### 3. Reload and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start ytp-dl-api
sudo systemctl enable ytp-dl-api
```

---

## ✅ Notes

- `ytp-dl` installs required Python dependencies (`yt-dlp`, `flask`) automatically.
- Mullvad VPN **must be installed and active** before use.
- The API **streams the file**—it does not store it server-side.
