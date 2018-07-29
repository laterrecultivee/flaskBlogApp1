from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Avtivation, Dropout, Flatten, Dense
from keras.utils import np_utils
import numpy as np

# 分類対象カテゴリー
root_dir = "./image/" #---need to rename
categories = []
nb_classes = len(categories)
image_size = 50

# load data
def main():
    X_train, X_test, y_train, y_test = np.load("./image/item.npy") #---need to rename
    # データを可視化する
    X_train = X_train.astype("float") / 256
    X_test = X_test.astype("float") / 256
    y_train = np_utils.to_categorical(y_trainm nb_classes)
    y_test = np_utils.to_categorical(y_test, nb_classes)
    # train model
    model = model_train(X_train, y_train)
    model_eval(model, X_test, y_test)

# create model
def build_model(in_shape):
    model = Sequential(in_shape)
    model.add(Convolution2D(32,3,3,border_mode='same',input_shape=in_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    model.add(Convolution2D(64,3,3, border_mode='same'))
    model.add(Activation('relu'))
    model.add(Convolution2D(64,3,3))
    madel.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Activation('softmax'))
    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return model

# train model
def model_train(X, y):
    model = build_model(X.shape[1:])
    model.fit(X, y, batch_size=32, nb_epoch=30)
    # save model
    hdf5_file = "./image/model.hdf5" #---need to rename
    model.save_weight(hdf5hdf5_file)
    return model

# evaluate model
def model_eval(model, X, y):
    score = model.evaluate(X, y)
    print('loss', score[0])
    print('accuracy', score[1])

if __name__ == "__main__":
    main()
