import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn import cross_validation
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from scipy.stats import gaussian_kde


df = pd.read_csv('reviews.csv',header=None)
#df.head()

index = 'review, uid, bid, active_life, arts_entertainment, automotive, beauty_spas, education, event_planning_services, financial_services, food, health_medical, home_services, hotels_travel, local_flavor, local_services, mass_media, nightlife, pets, professional_services, public_services_government, real_estate, religious_organizations, restaurants, shopping, weather, distance, daysOfWeek, isWeekend, month, season'.split(', ')
df.columns = index

y = df.review.map(float)
X = df.loc[:,index[1:]]
#scores = cross_validation.cross_val_score(model, X, y, cv=5, scoring='mean_squared_error')

from sklearn import cross_validation
N = y.shape[0]
kf = cross_validation.KFold(N, n_folds=5)
fold = 1 ; mse = []
for train_index, test_index in kf:
    print("FOLD:",fold,"TRAIN:", len(train_index), "TEST:", len(test_index)); fold+=1
    #X_train, X_test = X[train_index], X[test_index]
    #y_train, y_test = y[train_index], y[test_index]
    #print train_index
    #print test_index
    
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


i = 100000
xy = np.vstack([y_test[:i],y_pred[:i]])
z = gaussian_kde(xy)(xy)

fig, ax = plt.subplots()
ax.scatter(y_test[:i], y_pred[:i], c=z, s=10, edgecolor='')
plt.show()

#sorted(zip(model.feature_importances_,index[1:]),reverse=True)
