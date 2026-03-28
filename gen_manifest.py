import json
import pathlib
from pathlib import Path

"""
生成 manifest.json，列出所有照片和縮圖的相對 GitHub URLs
無需在前端呼叫 GitHub API，直接用靜態 JSON
"""

ROOT = Path(__file__).parent
PHOTO_DIR = ROOT / "WeddingPhoto"
THUMBS_DIR = PHOTO_DIR / "_thumbs"

# GitHub 配置（改成你的實際資訊）
GH_USER = "ZYXCYF"
GH_REPO = "WeddingAlbum"
GH_BRANCH = "main"
ALLOWED = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}

def get_github_url(rel_path):
    """相對路徑 → GitHub Raw URL"""
    return f"https://raw.githubusercontent.com/{GH_USER}/{GH_REPO}/{GH_BRANCH}/{str(rel_path).replace(chr(92), '/')}"

def get_jsdelivr_url(rel_path):
    """相對路徑 → jsDelivr CDN URL（比 GitHub Raw 更快更穩定）"""
    return f"https://cdn.jsdelivr.net/gh/{GH_USER}/{GH_REPO}@{GH_BRANCH}/{str(rel_path).replace(chr(92), '/')}"

def stem(name):
    """移除副檔名"""
    return name.rsplit(".", 1)[0].lower()

# 掃描照片
photos = []
if PHOTO_DIR.exists():
    # 先掃描所有照片
    all_files = sorted(PHOTO_DIR.glob("*"), key=lambda p: p.name.lower())
    
    # 建立縮圖 map
    thumb_map = {}
    if THUMBS_DIR.exists():
        for thumb_file in THUMBS_DIR.glob("*"):
            if thumb_file.is_file():
                thumb_map[stem(thumb_file.name)] = thumb_file
    
    # 只加入允許的圖片格式
    for photo_file in all_files:
        if photo_file.is_file() and photo_file.suffix.lower() in ALLOWED:
            s = stem(photo_file.name)
            rel_path = photo_file.relative_to(ROOT)
            
            # 優先用縮圖（如果存在），否則用原圖
            thumb = thumb_map.get(s)
            if thumb:
                thumb_rel = thumb.relative_to(ROOT)
                thumb_url = get_jsdelivr_url(thumb_rel)
            else:
                thumb_url = get_jsdelivr_url(rel_path)
            
            photos.append({
                "name": photo_file.name,
                "thumb": thumb_url,
                "full": get_jsdelivr_url(rel_path)
            })

# 寫出 manifest.json
manifest = {
    "version": 1,
    "photos": photos,
    "count": len(photos)
}

manifest_path = ROOT / "manifest.json"
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"✓ 已生成 manifest.json，包含 {len(photos)} 張照片")
print(f"  存放位置: {manifest_path}")
if photos:
    print(f"  範例: {photos[0]}")
