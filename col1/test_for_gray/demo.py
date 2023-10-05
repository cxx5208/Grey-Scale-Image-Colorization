# import the necessary packages
import os
import random

import cv2 as cv
import keras.backend as K
import numpy as np
import sklearn.neighbors as nn

from config import img_rows, img_cols
from config import nb_neighbors, T, epsilon
from model import build_model

if __name__ == '__main__':
    channel = 3

    model_weights_path = 'F:/mtech/col1/models/model.50-3.1305.hdf5'
    model = build_model()
    model.load_weights(model_weights_path)

    print(model.summary())

    image_folder = 'F:/mtech/col1/test_for_gray/gray_test/'
    names_file = 'F:/mtech/col1/test_for_gray/valid_names.txt'
    with open(names_file, 'r') as f:
        names = f.read().splitlines()

    #samples = random.sample(names, 11)

    h, w = img_rows//4, img_cols//4

    # Load the array of quantized ab value
    q_ab = np.load("F:/mtech/col1/data/pts_in_hull.npy")
    nb_q = q_ab.shape[0]

    # Fit a NN to q_ab
    nn_finder = nn.NearestNeighbors(n_neighbors=nb_neighbors, algorithm='ball_tree').fit(q_ab)

    for i in range(len(names)):
        image_name = names[i]
        filename = os.path.join(image_folder, image_name)
        print('Start processing image: {}'.format(filename))
        # b: 0 <=b<=255, g: 0 <=g<=255, r: 0 <=r<=255.
        
        gray = cv.imread(filename, 0)
        gray = cv.resize(gray, (img_rows, img_cols), cv.INTER_CUBIC)
        # L: 0 <=L<= 255, a: 42 <=a<= 226, b: 20 <=b<= 223.
        # print('np.max(L): ' + str(np.max(L)))
        # print('np.min(L): ' + str(np.min(L)))
        # print('np.max(a): ' + str(np.max(a)))
        # print('np.min(a): ' + str(np.min(a)))
        # print('np.max(b): ' + str(np.max(b)))
        # print('np.min(b): ' + str(np.min(b)))
        x_test = np.empty((1, img_rows, img_cols, 1), dtype=np.float32)
        x_test[0, :, :, 0] = gray / 255.

        # L: 0 <=L<= 255, a: 42 <=a<= 226, b: 20 <=b<= 223.
        X_colorized = model.predict(x_test)
        print(X_colorized.shape)
        X_colorized = X_colorized.reshape((h * w, nb_q))

        # Reweight probas
        X_colorized = np.exp(np.log(X_colorized + epsilon) / T)
        X_colorized = X_colorized / np.sum(X_colorized, 1)[:, np.newaxis]

        # Reweighted
        q_a = q_ab[:, 0].reshape((1, 313))
        q_b = q_ab[:, 1].reshape((1, 313))

        X_a = np.sum(X_colorized * q_a, 1).reshape((h, w))
        X_b = np.sum(X_colorized * q_b, 1).reshape((h, w))
        # print('np.max(X_a): ' + str(np.max(X_a)))
        # print('np.min(X_a): ' + str(np.min(X_a)))
        # print('np.max(X_b): ' + str(np.max(X_b)))
        # print('np.min(X_b): ' + str(np.min(X_b)))
        X_a = cv.resize(X_a, (img_rows, img_cols), cv.INTER_CUBIC)
        X_b = cv.resize(X_b, (img_rows, img_cols), cv.INTER_CUBIC)

        # Before: -90 <=a<= 100, -110 <=b<= 110
        # After: 38 <=a<= 228, 18 <=b<= 238
        X_a = X_a + 128
        X_b = X_b + 128
        # print('np.max(X_a): ' + str(np.max(X_a)))
        # print('np.min(X_a): ' + str(np.min(X_a)))
        # print('np.max(X_b): ' + str(np.max(X_b)))
        # print('np.min(X_b): ' + str(np.min(X_b)))

        out_lab = np.zeros((img_rows, img_cols, 3), dtype=np.int32)
        out_lab[:, :, 0] = gray[:, :]
        out_lab[:, :, 1] = X_a
        out_lab[:, :, 2] = X_b
        out_L = out_lab[:, :, 0]
        out_a = out_lab[:, :, 1]
        out_b = out_lab[:, :, 2]
        # print('np.max(out_L): ' + str(np.max(out_L)))
        # print('np.min(out_L): ' + str(np.min(out_L)))
        # print('np.max(out_a): ' + str(np.max(out_a)))
        # print('np.min(out_a): ' + str(np.min(out_a)))
        # print('np.max(out_b): ' + str(np.max(out_b)))
        # print('np.min(out_b): ' + str(np.min(out_b)))
        out_lab = out_lab.astype(np.uint8)
        #print(out_lab.shape)
        out_bgr = cv.cvtColor(out_lab, cv.COLOR_LAB2BGR)
        # print('np.max(out_bgr): ' + str(np.max(out_bgr)))
        # print('np.min(out_bgr): ' + str(np.min(out_bgr)))
        out_bgr = out_bgr.astype(np.uint8)


        cv.imwrite('F:/mtech/col1/test_for_gray/images/{}_image.png'.format(i), gray)
        cv.imwrite('F:/mtech/col1/test_for_gray/images/{}_out.png'.format(i), out_bgr)

    K.clear_session()