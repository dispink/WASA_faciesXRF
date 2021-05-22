import numpy as np 
import pandas as pd
from split import *

import datetime
date = datetime.datetime.now().strftime('%Y%m%d')

from time import perf_counter
start = perf_counter()

path = '/home/users/aslee/WASA_faciesXRF/'

data_df = pd.read_csv('{}data/XRF_ML_c.csv'.format(path))
X = data_df.iloc[:, 1:-2].values
y = data_df['facies_merge_2'].values
groups = data_df['core_section'].values

train_idx, test_idx = my_train_test_split(y, groups)
X_train = X[train_idx]
y_train = y[train_idx]
groups_train = groups[train_idx]

# This time I split the training set again to obtain dev set
trainn_idx, dev_idx = my_group_stratify_shuffle(X_train, y_train, groups_train)
X_trainn = X[train_idx[trainn_idx]]
X_dev = X[train_idx[dev_idx]]
y_trainn = y[train_idx[trainn_idx]]
y_dev = y[train_idx[dev_idx]]
groups_trainn = groups[train_idx[trainn_idx]]

del data_df, X, y, groups

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from split import my_group_stratify_shuffle_cv

print('LR')

pipe = Pipeline([
    ('scaling', StandardScaler()),
    ('pca', PCA()), 
    ('lr', LogisticRegression(max_iter = 10000, class_weight='balanced'))])

param_grid = [
    {'pca': [PCA(whiten=True)],
     'lr__C': np.logspace(-4, 5, 10)},
    {'pca': [None],
     'lr__C': np.logspace(-4, 5, 10)}
]

mycv = my_group_stratify_shuffle_cv(X_trainn, y_trainn, groups_trainn)

grid = GridSearchCV(pipe, param_grid = param_grid, cv = mycv, scoring = 'balanced_accuracy', n_jobs = -1)

grid.fit(X_trainn, y_trainn)

print("Best score on validation set: {:.2f}".format(grid.best_score_)) 
print("Best parameters: ", grid.best_params_)

pd.DataFrame(grid.cv_results_).to_csv('{}results/raw_lr_grid_{}.csv'.format(path, date))

from joblib import dump, load
dump(grid.best_estimator_, '{}models/raw_lr_model_{}.joblib'.format(path, date)) 

print("The computation takes {} hours.".format((perf_counter() - start)/3600))
