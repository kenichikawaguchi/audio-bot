import tempfile
import os
from github import Github
from datetime import datetime

from dotenv import load_dotenv


load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TMPDIR = os.getenv("TMPDIR")

# === 設定 ===
GITHUB_TOKEN = GITHUB_TOKEN  # ←ここに自分のトークンを入れる
REPO_NAME = "kenichikawaguchi/audio-bot"

# === GitHub 接続 ===
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)
print(TMPDIR)

# === 一時MP3ファイル作成（ここではダミー音声データ） ===
with tempfile.NamedTemporaryFile(dir=TMPDIR, delete=False, suffix=".mp3") as tmp:
    tmp.write(b"FAKE_MP3_DATA")  # 実際にはAIが生成した音声データを書き込む
    tmp_path = tmp.name

# === リリース作成 ===
tag_name = f"auto-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
release_name = f"AI Music {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
release = repo.create_git_release(tag_name, release_name, "自動生成された音声です。")

# === MP3アップロード ===
asset = release.upload_asset(tmp_path, name="music.mp3")
print("✅ MP3 uploaded to GitHub Release")

# === 公開URL作成 ===
public_url = f"https://github.com/{REPO_NAME}/releases/download/{tag_name}/music.mp3"
print("🌐 Public URL:", public_url)

# === 一時ファイル削除 ===
os.remove(tmp_path)
print("🧹 Local temp file deleted.")

