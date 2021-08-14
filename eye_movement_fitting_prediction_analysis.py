# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# Summary & overview of data sets
import matplotlib.pyplot as plt

training_data = pd.read_csv("/kaggle/input/emvic/train.csv")
test_data = pd.read_csv("/kaggle/input/emvic/test.csv")
print("training data shape: {}".format(training_data.shape))
print("training data column: {}".format(training_data.columns))
print("test data shape: {}".format(test_data.shape))
print("test data column: {}".format(test_data.columns))

# Overview of training data
print(training_data.info())
training_data.head(10)

# Overview of test data
print(test_data.info())
test_data.sample(5)

# Checking if there is any missing value in the data
def missing_values(df):
    for col in df.columns.tolist():
        if df[col].isnull().sum() > 0:
            print("{} has missing values: {}".format(col,df[col].isnull().sum()))
        
print(missing_values(training_data))
#left_range_96 = [*range(96)]
#training_data.drop(['class'],axis=1).iloc[0][left_range_96].plot.bar()

 a closer look at the data range where stimulus point disappeared from the middle of the screen
position_range = [*range(2048)]
stable_duration = [*range(int(1600/4))]
blank_duration_neighborhood = [*range(int(1600/4)-12,int((1600+20)/4)+24)]
stimulus_step = 12

fig, axes = plt.subplots(ncols=2, nrows=2,figsize=(20,20))
training_data.drop(['class'],axis=1).iloc[0][[len(position_range)*0 + idx for idx in blank_duration_neighborhood]].plot.bar(ax=axes[0][0])
training_data.drop(['class'],axis=1).iloc[0][[len(position_range)*1 + idx for idx in blank_duration_neighborhood]].plot.bar(ax=axes[0][1])
training_data.drop(['class'],axis=1).iloc[0][[len(position_range)*2 + idx for idx in blank_duration_neighborhood]].plot.bar(ax=axes[1][0])
training_data.drop(['class'],axis=1).iloc[0][[len(position_range)*3 + idx for idx in blank_duration_neighborhood]].plot.bar(ax=axes[1][1])

# a closer look at range of data where the stimulus points started to show on corners
fig, axes = plt.subplots(ncols=2, nrows=2, figsize=(20,20))
training_data.drop(['class'],axis=1).iloc[0][[*range(len(position_range)*0+420,len(position_range)*0 + 468)]].plot.bar(ax=axes[0][0])
training_data.drop(['class'],axis=1).iloc[0][[*range(len(position_range)*1+420,len(position_range)*1 + 468)]].plot.bar(ax=axes[0][1])
training_data.drop(['class'],axis=1).iloc[0][[*range(len(position_range)*2+420,len(position_range)*2 + 468)]].plot.bar(ax=axes[1][0])
training_data.drop(['class'],axis=1).iloc[0][[*range(len(position_range)*3+420,len(position_range)*3 + 468)]].plot.bar(ax=axes[1][1])

# a closer look at the data range where stimulus points stayed around the middle of the screen
fig, axes = plt.subplots(ncols=2, nrows=2, figsize=(20,20))
training_data.drop(['class'],axis=1).iloc[0][[*range(len(position_range)*0,len(position_range)*0 + 400)]].plot.bar(ax=axes[0][0])
training_data.drop(['class'],axis=1).iloc[0][[*range(len(position_range)*1,len(position_range)*1 + 400)]].plot.bar(ax=axes[0][1])
training_data.drop(['class'],axis=1).iloc[0][[*range(len(position_range)*2,len(position_range)*2 + 400)]].plot.bar(ax=axes[1][0])
training_data.drop(['class'],axis=1).iloc[0][[*range(len(position_range)*3,len(position_range)*3 + 400)]].plot.bar(ax=axes[1][1])

# correlation between columns
import seaborn as sn
correlation_training = training_data.drop(["class"],axis=1).corr()
sn.heatmap(correlation_training,cmap="YlGnBu")

# closeup at correlation_training
# lx - rx
sn.heatmap(correlation_training.iloc[len(position_range)+1:len(position_range)*2,0:len(position_range)],cmap='YlGnBu')

# closeup at correlation_training
# ly-ry
sn.heatmap(correlation_training.iloc[len(position_range)*3+1:,len(position_range)*2+1:len(position_range)*3],cmap='YlGnBu')

# generate dataframe of difference between consecutive test inputs for the training set
training_diff_data = pd.DataFrame(training_data['class'],columns=['class'])
for i in range(len(position_range)-1):
    training_diff_data['diff_lx_' + str(i)] = training_data.drop(['class'],axis=1).iloc[:,i+1] - training_data.drop(['class'],axis=1).iloc[:,i]
    
for i in range(len(position_range),2*len(position_range)-1):
    training_diff_data['diff_rx_' + str(i)] = training_data.drop(['class'],axis=1).iloc[:,i+1] - training_data.drop(['class'],axis=1).iloc[:,i]

for i in range(2*len(position_range),3*len(position_range)-1):
    training_diff_data['diff_ly_' + str(i)] = training_data.drop(['class'],axis=1).iloc[:,i+1] - training_data.drop(['class'],axis=1).iloc[:,i]
    
for i in range(3*len(position_range),4*len(position_range)-1):
    training_diff_data['diff_ry_' + str(i)] = training_data.drop(['class'],axis=1).iloc[:,i+1] - training_data.drop(['class'],axis=1).iloc[:,i]
    
training_diff_data.head(10)

# generate dataframe of difference between consecutive test inputs for the test set
test_diff_data = pd.DataFrame(test_data['class'],columns=['class'])
for i in range(len(position_range)-1):
    test_diff_data['diff_lx_' + str(i)] = test_data.drop(["class"],axis=1).iloc[:,i+1] - test_data.drop(['class'],axis=1).iloc[:,i]
    
for i in range(len(position_range),2*len(position_range)-1):
    test_diff_data['diff_rx_' + str(i)] = test_data.drop(["class"],axis=1).iloc[:,i+1] - test_data.drop(['class'],axis=1).iloc[:,i]
    
for i in range(2*len(position_range),3*len(position_range)-1):
    test_diff_data['diff_ly_' + str(i)] = test_data.drop(["class"],axis=1).iloc[:,i+1] - test_data.drop(['class'],axis=1).iloc[:,i]
    
for i in range(3*len(position_range),4*len(position_range)-1):
    test_diff_data['diff_ry_' + str(i)] = test_data.drop(["class"],axis=1).iloc[:,i+1] - test_data.drop(['class'],axis=1).iloc[:,i]
    
test_diff_data.head(5)

# plot the heatmap for the new variables calculated from difference
correlation_training_diff = training_diff_data.drop(['class'],axis=1).corr()
sn.heatmap(correlation_training_diff,cmap="YlGnBu")

# a closer look at the block on the heatmap of correlation,
# where the correlation between the x coordinates of left eye and right eye are calcualted
sn.heatmap(correlation_training_diff.iloc[:len(position_range),:len(position_range)],cmap="YlGnBu")

# a closer look at the block on the heatmap of correlation,
# where the correlation between the y coordinates of left eye and right eye are calcualted
sn.heatmap(correlation_training_diff.iloc[2*len(position_range):3*len(position_range),2*len(position_range):3*len(position_range)],cmap="YlGnBu")

from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# train the models using the original training data
# two kernels are used in the SVC model: (1) rbf and (2) linear
training_y = training_data['class'].to_numpy()
training_x = training_data.drop(['class'],axis=1).to_numpy()
clf_svc_rbf = make_pipeline(StandardScaler(),SVC())
clf_svc_rbf.fit(training_x, training_y)

clf_svc_linear = make_pipeline(StandardScaler(),LinearSVC(random_state=0,tol=1e-5))
clf_svc_linear.fit(training_x,training_y)

# predit the result using the two kernels
test_x = test_data.drop(['class'],axis=1).to_numpy()
# SVC RBF
output_rbf = clf_svc_rbf.predict(test_x)
# linearSVC
output_linear = clf_svc_linear.predict(test_x)

import collections
# the ratio of different classified result between RBF kernel and linear kernel
print(np.sum(output_rbf == output_linear)/output_rbf.size)
# group the difference between two kernel by the user ID
deviation_stats = collections.Counter(output_rbf[output_rbf != output_linear])
print(deviation_stats)
plt.bar(deviation_stats.keys(),deviation_stats.values())
plt.xticks(np.arange(1, 38))
plt.xlabel("User ID")
plt.title("Analysis on Devation between Linear and RBF kernel for original data set")
plt.show()

# train the models using the calculated training data (difference)
# two kernels are used in the SVC model: (1) rbf and (2) linear
training_diff_y = training_diff_data['class'].to_numpy()
training_diff_x = training_diff_data.drop(['class'],axis=1).to_numpy()
# RBF kernel
clf_diff_svc_rbf = make_pipeline(StandardScaler(),SVC())
clf_diff_svc_rbf.fit(training_diff_x,training_diff_y)

# Linear kernel
clf_diff_svc_linear = make_pipeline(StandardScaler(),LinearSVC(random_state=0,tol=1e-5))
clf_diff_svc_linear.fit(training_diff_x, training_diff_y)

# preditc the result of diff data using the two kernel
test_diff_x = test_diff_data.drop(['class'],axis=1).to_numpy()
# RBF kernel
output_diff_rbf = clf_diff_svc_rbf.predict(test_diff_x)
# linear kernel
output_diff_linear = clf_diff_svc_linear.predict(test_diff_x)

# the ratio of different classified result between RBF kernel and linear kernel
print(np.sum(output_diff_rbf == output_diff_linear)/output_diff_rbf.size)
# plot the stats of which user 
deviation_stats_diff = collections.Counter(output_diff_rbf[output_diff_rbf != output_diff_linear])
print(deviation_stats_diff)
plt.bar(deviation_stats_diff.keys(),deviation_stats_diff.values())
plt.xticks(np.arange(1,38))
plt.title("Analysis on Devation between Linear and RBF kernel for Diff Data set")
plt.xlabel("User ID")
plt.show()

print(np.sum(output_rbf == output_diff_rbf)/output_rbf.size)
deviation_stats_two_analysis = collections.Counter(output_rbf[output_rbf != output_diff_rbf])
print(deviation_stats_two_analysis)
plt.bar(deviation_stats_two_analysis.keys(),deviation_stats_two_analysis.values())
plt.xticks(np.arange(1,38))
plt.title("Analysis on Devation between Original and Diff Data sets")
plt.xlabel("User ID")
plt.show()
