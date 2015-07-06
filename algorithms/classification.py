from __future__ import absolute_import
from __future__ import print_function
import numpy as np

from keras.preprocessing import sequence
from keras.optimizers import SGD, RMSprop, Adagrad
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, TimeDistributedDense
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU
#from keras.datasets import imdb

def build_model_basic():
    print('Build model basic...')
    model = Sequential()
    model.add(TimeDistributedDense(30, 512, init='he_normal'))
    model.add(Dropout(0.5))
    model.add(LSTM(512, 128, activation='hard_sigmoid', return_sequences=True))
    model.add(LSTM(128, 6, activation='hard_sigmoid'))
    model.add(Activation('hard_sigmoid'))
    # model.add(Embedding(max_features, 256))    
    # 
    # model.add(Dense(128, 1))

    return model
#user id, venue id, categories, weather, distance, day of week, month, isweekend, season
def parseline(line):
    aux_array = []
    rating = int(line[:line.index(' [')])
    line = line[line.index('['):]
    
    #removing break lines
    line = line.replace('\n', '')
    #removing brackets
    line = line.replace('[','').replace(']','')

    #parsing string to int and append to array
    for x in line.split(','):
        aux_array.append(int(x))
    
    return aux_array, rating

def generate_data():
    x = []
    y = []

    filename = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/theano/reviews.data'
    f = open(filename)    
    for line in f:
       features, rating = parseline(line)
       x.append(features)
       y.append(rating)
    
    return x, y

def run():
    model = build_model_basic()

    print('compiling...')
    model.compile(loss='categorical_crossentropy', optimizer='adam', class_mode="categorical")

    print('loading data...')
    x, y = generate_data()
    
    print('creating trainning and test data')
    x_train = np.asarray(x[:150000])
    x_train = x_train[:, np.newaxis, :]    
    y_train = np_utils.to_categorical(y[:150000])
    
    x_test = np.asarray(x[150000:])
    x_test = x_test[:, np.newaxis, :]
    y_test = np_utils.to_categorical(y[150000:])

    print('trainning')
    model.fit(x_train, y_train, nb_epoch=10, batch_size=256)
    
    print('testing...')
    score = model.evaluate(x_test, y_test, batch_size=256)
    print(score)
    
    print('predicting...')
    values = model.predict(x_test, batch_size=256, verbose=1)
    np.savetxt('prediction.txt', values)

    values = model.predict_classes(x_test, batch_size=256, verbose=1)
    np.savetxt('prediction-classes.txt', values)
    print(values)
    

    return

if __name__ == '__main__':
    run()