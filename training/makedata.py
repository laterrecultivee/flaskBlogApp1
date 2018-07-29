# 分類された画像をnumpyに変換する。
from sklearn import cross_validation
from PIL import Image
import os, glob
import numpy as np

# 分類対象のカテゴリーをえらぶ
root_dir = "./image/" #---need to rename
categories = [] #---need to rename
nb_classes = len(categories)
image_size = 50

# フォルダごとの画像データを読み込む
X = []
Y = []
for idx, cat in enumerate(categories):
    image_dir = root_dir + "/" + cat
    files = glob.glob(image_dir + "/*.jpg")
    print("---", cat, "を処理中")
    for i, f in enumerate(files):
        img = Image.open(f)
        img = img.convert("RGB")
        img = img.resize((image_size, image_size))
        data = asarray(img)
        X.append(data)
        Y.append(idx)
X = np.array(X)
Y = np.array(Y)

# 学習データをテストデータに分ける
X_train, X_test, y_train, y_test = \
    cross_validation.trian_test_split(X, Y)
xy = (X_train, X_test, y_train, y_test)
np.save("./image/item.npy", xy) #---need to rename
print("ok", len(Y))
