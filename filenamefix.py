#幫我修改目錄.\WeddingPhotos\裡的檔案名稱，將檔案名稱中2026改成ZYXCYF
import os

directory = r".\WeddingPhoto"
for filename in os.listdir(directory):
    if "-" in filename:
        new_filename = filename.replace("-", "_")
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
