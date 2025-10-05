import os
from github import Github, Auth
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# === 設定 ===
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "kenichikawaguchi/audio-bot"
TMPDIR = os.getenv("TMPDIR", "/tmp")  # TMPDIR 環境変数がなければ /tmp を使用
MP3_FILENAME = "einekleine.mp3"  # アップロードする実際の MP3 ファイル名

# === GitHub 接続 ===
g = Github(auth=Auth.Token(GITHUB_TOKEN))
repo = g.get_repo(REPO_NAME)

# === MP3 ファイルのパス ===
mp3_path = os.path.join(TMPDIR, MP3_FILENAME)
if not os.path.exists(mp3_path):
    raise FileNotFoundError(f"{mp3_path} が見つかりません")

# === リリース作成 ===
tag_name = f"auto-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
release_name = f"AI Music {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

release = repo.create_git_release(
    tag_name,
    release_name,
    "自動生成された音声です。",
    draft=False,
    prerelease=False
)

# === MP3 アップロード ===
asset = release.upload_asset(mp3_path, name=MP3_FILENAME)
print("✅ MP3 uploaded to GitHub Release")

# === 公開 URL 作成 ===
public_url = f"https://github.com/{REPO_NAME}/releases/download/{tag_name}/{MP3_FILENAME}"
print("🌐 Public URL:", public_url)

# === 一時ファイル削除 ===
os.remove(mp3_path)
print("🧹 Local temp file deleted.")


