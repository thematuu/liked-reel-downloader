import os
import json
import subprocess
from datetime import datetime
import re
import argparse
from dotenv import load_dotenv

load_dotenv()

def load_downloaded(path):
    if not os.path.exists(path):
        return set()
    with open(path, 'r') as f:
        return set(line.strip() for line in f)

def save_downloaded(code, path):
    with open(path, 'a') as f:
        f.write(code + '\n')

def sanitize_filename(s):
    return re.sub(r'[^\w\-_. ()]', '', s).strip()

def extract_reel_links(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    reels = []
    for entry in data.get("likes_media_likes", []):
        username = entry.get("title", "unknown")
        for item in entry.get("string_list_data", []):
            url = item.get("href", "")
            if "/reel/" in url:
                cleaned_url = url.split('?')[0].rstrip('/')
                code = cleaned_url.split('/reel/')[-1]
                timestamp = item.get("timestamp", 0)
                time_str = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H-%M-%S')

                reels.append({
                    "url": cleaned_url,
                    "username": sanitize_filename(username),
                    "time_str": time_str,
                    "code": code
                })
    return reels

def download_reel(reel, cookies_file, download_dir, proxy, retries=3):
    filename = f"{reel['username']} - {reel['time_str']}.mp4"
    output_template = os.path.join(download_dir, filename)

    print(f"⬇️ Downloading: {reel['url']} → {output_template}")
    if not os.path.exists(cookies_file):
        print(f"❌ Missing required cookies file: {cookies_file}")
        return False

    command = [
        'yt-dlp',
        '--cookies', cookies_file,
        '-o', output_template,
        reel['url']
    ]

    if proxy:
        command.extend(['--proxy', proxy])

    attempt = 0
    while attempt < retries:
        try:
            subprocess.run(command, check=True)
            print("✅ Downloaded successfully.")
            return True
        except subprocess.CalledProcessError as e:
            attempt += 1
            print(f"⚠️ Attempt {attempt} failed: {e}")
            if attempt < retries:
                print("🔁 Retrying...")
            else:
                print("❌ All attempts failed.")

    return False

def main():
    parser = argparse.ArgumentParser(description="Download liked Instagram Reels")
    parser.add_argument('--liked-json', default=os.getenv('LIKED_JSON', 'liked_posts.json'), help='Path to liked_posts.json')
    parser.add_argument('--downloaded-file', default=os.getenv('DOWNLOADED_FILE', 'downloaded_reels.txt'), help='File to store downloaded codes')
    parser.add_argument('--cookies-file', default=os.getenv('COOKIES_FILE', 'cookies.txt'), help='Path to cookies.txt')
    parser.add_argument('--download-dir', default=os.getenv('DOWNLOAD_DIR', 'downloads'), help='Directory to save downloaded videos')
    parser.add_argument('--proxy', default=os.getenv('PROXY'), help='Proxy URL (e.g. http://user:pass@host:port)')

    args = parser.parse_args()

    os.makedirs(args.download_dir, exist_ok=True)

    if not os.path.exists(args.liked_json):
        print(f"❌ JSON file not found: {args.liked_json}")
        return

    downloaded_codes = load_downloaded(args.downloaded_file)
    reel_items = extract_reel_links(args.liked_json)

    new_downloads = 0
    for reel in reel_items:
        if reel['code'] in downloaded_codes:
            print(f"⏭️ Skipping already downloaded: {reel['code']}")
            continue

        if download_reel(reel, args.cookies_file, args.download_dir, args.proxy):
            save_downloaded(reel['code'], args.downloaded_file)
            new_downloads += 1

    print(f"\n🎉 Done. New Reels downloaded: {new_downloads}")

if __name__ == "__main__":
    main()