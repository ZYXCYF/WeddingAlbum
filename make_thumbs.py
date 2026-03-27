import os, pathlib
from PIL import Image, ImageOps

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
                # 修正 EXIF 方向
                im = ImageOps.exif_transpose(im)

                # 若為動畫（多格），取第一格做縮圖
                is_animated = getattr(im, "is_animated", False) or getattr(im, "n_frames", 1) > 1
                if is_animated:
                    try:
                        im.seek(0)
                    except Exception:
                        pass

                # 若有 alpha 或調色盤，轉為 RGB（JPG 不支援透明）
                im = im.convert("RGB") if im.mode in ("RGBA","P","LA") else im
                w, h = im.size
                if w > MAX_W:
                    nh = int(h * (MAX_W / w))
                    im = im.resize((MAX_W, nh), Image.LANCZOS)

                # 優先輸出 JPG（瀏覽器支援佳、體積小）
                out = out.with_suffix(".jpg")
                im.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)
                count += 1
                print("OK", out.name)
        except Exception as e:
            print("SKIP", p.name, e)

print(f"done, {count} thumbs")
