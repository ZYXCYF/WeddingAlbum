#幫我修改目錄.\WeddingPhotos\裡的檔案名稱，將檔案名稱中2026改成ZYXCYF
import os

directory = r".\WeddingPhoto"
for filename in os.listdir(directory):
    if "2026" in filename:
        new_filename = filename.replace("2026", "ZYXCYF")
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
