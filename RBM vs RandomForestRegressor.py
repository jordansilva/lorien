
# coding: utf-8

# In[46]:

import sys
import numpy as np
from util.reader import reader
from scipy.ndimage import convolve
from sklearn import linear_model, datasets, metrics, cross_validation, preprocessing
from sklearn.cross_validation import train_test_split
from sklearn.neural_network import BernoulliRBM
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

dataset = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/vector.rbm'

r = reader(dataset)
data, labels, data_full = r.load(size=sys.maxsize, progress=False)


# In[144]:

from sklearn.metrics import mean_squared_error
from numpy.random import RandomState

# data2 = []
# for d in data:
#     data2.append(d[:24])
print('starting')
X = np.asarray(data2, 'int32')
y = np.asarray(labels, 'int32')
N = len(y)
kf = cross_validation.KFold(N, n_folds=5)
fold = 1 ; mae = []; rmse = [];

sgd = linear_model.SGDClassifier()
prng = RandomState()
rbm = BernoulliRBM(verbose=True, batch_size=128, learning_rate=0.06, n_iter=20, n_components=256)

prng2 = RandomState()
rbm2 = BernoulliRBM(random_state=prng2, verbose=True, batch_size=100, learning_rate=0.08, n_iter=20, n_components=5)

classifier = Pipeline(steps=[('rbm', rbm), ('rbm2', rbm2), ('sgd', sgd)])

for train_index, test_index in kf:
    print("FOLD:",fold,"TRAIN:", len(train_index), "TEST:", len(test_index)); fold+=1
    X_train = X[train_index]
    y_train = y[train_index]

    X_test = X[test_index]
    y_test = y[test_index]
    
    #logistic = linear_model.LogisticRegression()
    #logistic.C = 6000.0

    #classifier = Pipeline(steps=[('rbm', rbm), ('sgd', sgd)])
    #classifier = Pipeline(steps=[('rbm', rbm), ('rbm2', rbm2), ('sgd', sgd)])

    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)    
    mae.append(mean_absolute_error(y_test,y_pred))
    rmse.append(math.sqrt(mean_squared_error(y_test,y_pred)))
    print mae
    print rmse
    
print("MAE: ", sum(mae)/len(mae))
print("RMSE: ", sum(rmse)/len(rmse))


# In[155]:

import math
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_absolute_error

print('starting')
X = np.asarray(data, 'float32')
y = np.asarray(labels, 'float32')
N = len(y)
kf = cross_validation.KFold(N, n_folds=5)
fold = 1 ; rmse = []; mae = [];
#model = RandomForestRegressor(n_estimators=100, n_jobs=4) # n_jobs=4
model = RandomForestClassifier(n_estimators=300, n_jobs=4) # n_jobs=4    
for train_index, test_index in kf:
    X_train = X[train_index]
    y_train = y[train_index]

    X_test = X[test_index]
    y_test = y[test_index]

    print("FOLD:",fold,"TRAIN:", len(X_train), "TEST:", len(y_test)); fold+=1


    model.fit(X_train,y_train)

    y_pred = model.predict(X_test)
    mae.append(mean_absolute_error(y_test,y_pred))
    rmse.append(math.sqrt(mean_squared_error(y_test,y_pred)))

print("RMSE: ", sum(rmse)/len(rmse))
print("MAE: ", sum(mae)/len(mae))


# In[ ]:



