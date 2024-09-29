from face_detected.retinaface import Retinaface
import os
import sys
from pathlib import Path
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

retinaface = Retinaface()


# 人脸编码
list_dir = os.listdir(ROOT / "face_db/train_datasets")
print("=" * 50)
print("list of name...")
print(list_dir)
print("=" * 50)
image_paths = []
names = []
student_IDs = []
print(list_dir)
for name in list_dir:
    if name == ".DS_Store":
        # 防止Macos隐藏文件
        continue
    image_paths.append(str(ROOT) + "/face_db/train_datasets/" + name)
    names.append(name.split("_")[0])
    student_IDs.append(name.split("_")[1])
print(image_paths)
print(names)
print(student_IDs)
retinaface.encode_face_dataset(image_paths, names, student_ID=student_IDs)
print("face_encoding successful!")