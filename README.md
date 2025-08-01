# Liked Reel Downloader

Download all the Instagram Reels you've liked using your `liked_posts.json` (from Instagram's Account Center export) and `yt-dlp`.

This script ensures previously downloaded Reels are skipped, proxy support, and configurable paths via CLI or `.env`.

---

## Features

- Parses `liked_posts.json` to extract Reel URLs
- Downloads Reels using [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Stores videos in a custom or default `downloads/` folder
- File names use: `{username} - {YYYY-MM-DD HH-MM-SS}.mp4`
- Avoids re-downloading the same Reels
- Configurable via `.env` or command-line arguments
- Optional proxy
- Uses `cookies.txt` for Instagram authenticated access

---

## Installation

### 1. Download the Project

You can either:

#### Option 1: Clone via Git

```bash
git clone https://github.com/thematuu/liked-reel-downloader.git
cd liked-reel-downloader
```

#### Option 2: Download ZIP

- Visit: https://github.com/thematuu/liked-reel-downloader
- Click the green **"Code"** button
- Select **"Download ZIP"**
- Unzip and open the folder

---

### 2. Install Requirements

You need:

- Python **3.8+**
- `yt-dlp` and `python-dotenv`

To install dependencies:

```bash
pip install -r requirements.txt
```

## Setup

### 1. Download your Instagram data

Go to: https://accountscenter.instagram.com/info_and_permissions/

Then choose:

- **Account Center**
- **Your Information and Permissions**
- **Download your information**
- **Download or transfer information**
- **Some of your information**
- **Likes**
- **Download to device**
- **Select Data range**
- **Format JSON**
- **Create files**

Unzip the file and place `liked_posts.json` into this project folder (or configure its location with CLI or `.env`).

---

### 2. Export Instagram cookies

Instagram requires login to access all Reel content. You must export your cookies.

> **Tip**: To reduce any risk of account issues, consider using an **alternate account** for downloading. I haven’t had problems, but it’s better to be cautious.

#### Recommended extensions:

> ⚠️ **Disclaimer**: These are third-party browser extensions. Use at your own discretion. I am **not responsible** for their security, privacy, or behavior.

- **Chrome**: [Get cookies.txt Locally](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
- **Firefox**: [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

After exporting, save the file as `cookies.txt` in the project folder (or specify another location via CLI or `.env`).

---

### 3. (Optional) Use a Proxy

Instagram may block requests depending on your IP address or region. You can route requests through a proxy if needed.

You can configure the proxy in two ways:

#### Option 1: Set via `.env` file

Create or edit a `.env` file in your project folder:

```env
PROXY=http://username:password@proxyhost:port
```

This will automatically be picked up when you run the script.

#### Option 2: Pass via command-line

You can override the proxy using a CLI argument:

```bash
python main.py --proxy http://username:password@proxyhost:port
```

---

If you're not using a proxy, you can skip this step.


## Usage

By default, just run:

```bash
python main.py
```

It will use these **default values** unless overridden:

| Setting             | Default Value             | Override via |
|---------------------|---------------------------|--------------|
| Liked JSON file     | `liked_posts.json`        | `--liked-json`, `.env` |
| Downloaded tracker  | `downloaded_reels.txt`    | `--downloaded-file`, `.env` |
| Cookies file        | `cookies.txt`             | `--cookies-file`, `.env` |
| Download folder     | `downloads/`              | `--download-dir`, `.env` |
| Proxy               | *(none)*                  | `--proxy`, `.env` |

---

### Command-Line Options

Example with full customization:

```bash
python main.py \
  --liked-json data/liked_posts.json \
  --cookies-file auth/cookies.txt \
  --download-dir ig/saved_reels \
  --downloaded-file logs/downloaded_reels.txt \
  --proxy http://username:password@proxyhost:port
```

---

## Example Output

```
downloads/
├── exampleusername - 2025-08-01 13-54-55.mp4
├── anotheruser - 2025-08-01 14-02-13.mp4
```

A file called `downloaded_reels.txt` will track which Reels you've already downloaded.  
> To redownload everything from scratch, simply **delete or empty this file**.

---

## Disclaimer

This tool is intended for **personal use only** with your own Instagram account and exported data.

It uses `cookies.txt` to simulate logged-in sessions. Do not use this tool to violate Instagram’s [Terms of Service](https://help.instagram.com/581066165581870).
