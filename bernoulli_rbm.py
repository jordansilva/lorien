"""
==============================================================
Restricted Boltzmann Machine features for digit classification
==============================================================

For greyscale image data where pixel values can be interpreted as degrees of
blackness on a white background, like handwritten digit recognition, the
Bernoulli Restricted Boltzmann machine model (:class:`BernoulliRBM
<sklearn.neural_network.BernoulliRBM>`) can perform effective non-linear
feature extraction.

In order to learn good latent representations from a small dataset, we
artificially generate more labeled data by perturbing the training data with
linear shifts of 1 pixel in each direction.

This example shows how to build a classification pipeline with a BernoulliRBM
feature extractor and a :class:`LogisticRegression
<sklearn.linear_model.LogisticRegression>` classifier. The hyperparameters
of the entire model (learning rate, hidden layer size, regularization)
were optimized by grid search, but the search is not reproduced here because
of runtime constraints.

Logistic regression on raw pixel values is presented for comparison. The
example shows that the features extracted by the BernoulliRBM help improve the
classification accuracy.
"""

from __future__ import print_function

print(__doc__)

# Authors: Yann N. Dauphin, Vlad Niculae, Gabriel Synnaeve
# License: BSD

import sys
import numpy as np
import matplotlib.pyplot as plt

from util.reader import reader
from scipy.ndimage import convolve
from sklearn import linear_model, datasets, metrics, cross_validation, preprocessing
from sklearn.cross_validation import train_test_split
from sklearn.neural_network import BernoulliRBM
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline


###############################################################################
# Setting up

class Bernoulli:

    dataset = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/vector.rbm'

    def __init__(self):
        r = reader(self.dataset)
        self.data, self.labels, self.data_full = r.load(size=sys.maxsize, progress=False)

    def run(self):
        # Load Data
        X = np.asarray(self.data, 'float32')
        # X, Y = nudge_dataset(X, labels)
        # X = (X - np.min(X, 0)) / (np.max(X, 0) + 0.0001)  # 0-1 scaling

        X_train, X_test, Y_train, Y_test = train_test_split(X, self.labels,
                                                            test_size=0.2,
                                                            random_state=0)

        N = len(self.labels)
        kf = cross_validation.KFold(N, n_folds=5)
        fold = 1 ; mse = []
        for train_index, test_index in kf:
            print("FOLD:",fold,"TRAIN:", len(train_index), "TEST:", len(test_index)); fold+=1
            
            X_train = X.iloc[train_index]
            y_train = y.iloc[train_index]
            
            X_test = X.iloc[test_index]
            y_test = y.iloc[test_index]
            
            model = RandomForestRegressor(n_estimators=10, n_jobs=4) # n_jobs=4
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            
            mse.append( mean_squared_error(y_test,y_pred) )
            print mse[-1]

        sum(mse)/len(mse)


        # Models we will use
        logistic = linear_model.LogisticRegression()
        logistic.C = 6000.0

        sgd = linear_model.SGDClassifier()

        binarizer = preprocessing.LabelBinarizer()


        rbm = BernoulliRBM(random_state=0, verbose=True, batch_size=500, learning_rate=0.08, n_iter=20, n_components=256)
        rbm2 = BernoulliRBM(random_state=0, verbose=True, batch_size=500, learning_rate=0.1, n_iter=10, n_components=100)
        randomforest = RandomForestRegressor(n_estimators=10, n_jobs=4) # n_jobs=4

        classifier = Pipeline(steps=[('rbm', rbm), ('rbm2', rbm2), ('sgd', sgd)])

        ###############################################################################
        # Training

        # Hyper-parameters. These were set by cross-validation,
        # using a GridSearchCV. Here we are not performing cross-validation to
        # save time.
        # More components tend to give better prediction performance, but larger
        # fitting time

        # Training RBM-Logistic Pipeline
        classifier.fit(X_train, Y_train)

        # Training Logistic regression
        # logistic_classifier = linear_model.LogisticRegression(C=100.0)
        # logistic_classifier.fit(X_train, Y_train)

        ###############################################################################
        # Evaluation

        print()
        print("Logistic regression using RBM features:\n%s\n" % (
            metrics.classification_report(
                Y_test,
                classifier.predict(X_test))))

        # print("Logistic regression using raw pixel features:\n%s\n" % (
        #     metrics.classification_report(
        #         Y_test,
        #         logistic_classifier.predict(X_test))))

        ###############################################################################
        #plt.figure(figsize=(4.2, 4))
        # for i, comp in enumerate(rbm.components_):
        #     plt.subplot(10, 10, i + 1)
        #     plt.imshow(comp.reshape((8, 8)), cmap=plt.cm.gray_r,
        #                interpolation='nearest')
        #     plt.xticks(())
        #     plt.yticks(())
        # plt.suptitle('100 components extracted by RBM', fontsize=16)
        # plt.subplots_adjust(0.08, 0.02, 0.92, 0.85, 0.08, 0.23)

        plt.show()
        return

if __name__ == '__main__':
    b = Bernoulli()
    b.run()