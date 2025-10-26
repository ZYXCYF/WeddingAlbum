import os, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).parent
SRC  = ROOT / "WeddingPhoto"
DST  = SRC / "_thumbs"
DST.mkdir(exist_ok=True)

MAX_W = 1280   # 縮圖寬度（可調 800~1600）
QUALITY = 82   # webp 品質（越高越清晰、檔案越大）

exts = {".jpg",".jpeg",".png",".webp",".avif",".gif"}
count = 0

for p in SRC.iterdir():
    if p.is_file() and p.suffix.lower() in exts:
        out = DST / p.name  # 與原圖同名（副檔名保留）
        try:
            with Image.open(p) as im:
                im = im.convert("RGB") if im.mode in ("RGBA","P","LA") else im
                w, h = im.size
                if w > MAX_W:
                    nh = int(h * (MAX_W / w))
                    im = im.resize((MAX_W, nh), Image.LANCZOS)
                # 優先輸出 webp（瀏覽器支援佳、體積小）
                out = out.with_suffix(".webp")
                im.save(out, "WEBP", quality=QUALITY, method=6)
                count += 1
                print("OK", out.name)
        except Exception as e:
            print("SKIP", p.name, e)

print(f"done, {count} thumbs")
