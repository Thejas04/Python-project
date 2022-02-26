# import libraries
import unittest
from matplotlib import collections
import pandas as pd
import os
from math import sqrt
import matplotlib.pyplot as plt
import seaborn as sns
from db_loader import define_session, Load_Data
from db.schemas import test, train
import warnings
warnings.filterwarnings("ignore")


# finds ideal functiona and applies it to test data
class best_function(object):
    
    # parent folder containing data
    CSV_PATH = '../data'

    #reading all the csv data
    def __init__(self, train_path, ideal_path, test_path):
        
        try:
            self.df_train = pd.read_csv(os.path.join(self.CSV_PATH, train_path))
            self.df_ideal = pd.read_csv(os.path.join(self.CSV_PATH, ideal_path))
            self.df_test = pd.read_csv(os.path.join(self.CSV_PATH, test_path))
        except FileNotFoundError:
            print('File Not Found')

    # finds 4 ideal function for the training set
    def ideal_function(self):
        
        train_x, train_y = self.df_train['x'].to_list(), self.df_train.drop('x', axis=1)
        ideal_x, ideal_y = self.df_ideal['x'].to_list(), self.df_ideal.drop('x', axis=1)

        x_mean = sum(ideal_x) / len(ideal_x)
        self.best_fit = []
        
        # iterates over all the trianing 'y' data
        for i in train_y.columns:
            mini = 999999999999999999
    
            for j in ideal_y.columns:
                y_h = ideal_y[j].to_list()
                y_h_mean = sum(y_h) / len(y_h)  
                sum_ = 0
                
                # least square calculation
                for x,y in zip(train_x, train_y[i]):
                    sum_ += sqrt( pow( x-x_mean, 2) + pow( y-y_h_mean, 2) )
                sum_ /= len(train_x)
                
                if sum_ < mini:
                    mini = sum_
                    idx = j
                    
            self.best_fit.append(idx)        
        
        return x_mean
    
    # finds the ideal function of each sample of the test-set
    def test_function(self, x_mean):

        y_mean, self.best_func, self.deviation = [], [], []
        ideal_x, ideal_y = self.df_ideal['x'].to_list(), self.df_ideal.drop('x', axis=1)
        best_fit_ = ideal_y[self.best_fit]
        
        # calculates mean of the ideal function
        for y in best_fit_.columns:
            temp = best_fit_[y].to_list()
            y_mean.append(sum(temp)/len(temp))
        
        try:
            for x,y in zip(self.df_test['x'].to_list(), self.df_test['y'].to_list()):
                
                mini = 999999999999999999
                
                for y_f,j in zip(y_mean, best_fit_.columns):
                    
                    # least square
                    temp = sqrt( pow( x-x_mean, 2) + pow( y-y_f, 2) )
                    if temp < mini:
                        mini = temp
                        idx = j
                
                self.best_func.append(idx)
                self.deviation.append(mini)
        except:
            pass
        
        # final result is stored here
        df_result = pd.DataFrame(list(zip(self.deviation, self.best_func)), columns=['Deviation', 'Ideal function'])
       
        df_result['x'] = self.df_test['x']
        df_result['y'] = self.df_test['y']
        return df_result
    

# helps in visualization
class visualize_(best_function):
    
    #plot scatter and line plots 
    def visualizations(self):

        fig, ax = plt.subplots(2, 2, figsize=(20, 20))
        k = 0
        lbl = list(self.df_train.drop('x', axis=1).columns)
        
        # train-set and ideal function plot
        for i in range(2):
            for j in range(2):
                ax[i][j].scatter(self.df_train['x'].to_list(), self.df_train[lbl[k]].to_list(), label="train data")
                ax[i][j].plot(self.df_ideal['x'].to_list(), self.df_ideal[self.best_fit[k]].to_list(), label="ideal function")
                ax[i][j].set_xlabel('x')
                ax[i][j].set_ylabel('y')
                ax[i][j].legend()
                k += 1

        
        fig, ax = plt.subplots(2, 2, figsize=(20, 20))
        k = 0
        
        # test-set and ideal function plot
        for i in range(2):
            for j in range(2):
                x = df_result[df_result['Ideal function'] == self.best_fit[k]]['x'].to_list()
                y = df_result[df_result['Ideal function'] == self.best_fit[k]]['y'].to_list()
                
                ax[i][j].scatter(x, y, label="test data")
                ax[i][j].plot(self.df_ideal['x'].to_list(), self.df_ideal[self.best_fit[k]].to_list(), label="ideal function")
                ax[i][j].set_xlabel('x')
                ax[i][j].set_ylabel('y')
                ax[i][j].legend()
                k += 1

        plt.show()




def load_csv_dataset(s):

    CSV_PATH = '../data'
    
    # for train set
    try:
        file_name = os.path.join(CSV_PATH, "train.csv") 
        data = Load_Data(file_name) 

        for i in data:
            record = train.Train(**{
                'x' :i[0],
                'y1' : i[1],
                'y2' : i[2],
                'y3' : i[3],
                'y4' : i[4],
            })
            s.add(record) 
        s.commit()
    except:
        s.rollback()
    finally:
        s.close()
        
    # for test set
    try:
        file_name = os.path.join(CSV_PATH, "test.csv") 
        data = Load_Data(file_name) 

        for i in data:
            record = test.Test(**{
                'x' :i[0],
                'y1' : i[1],
            })
            s.add(record) 
        s.commit()
    except:
        s.rollback()
    finally:
        s.close()



# create an object of child class to invoke methods and access an object
obj = visualize_('train.csv', 'ideal.csv', 'test.csv')

# finds ideal function
x_mean = obj.ideal_function()

# for testing
df_result = obj.test_function(x_mean)

# prints first five sample of the obtained result
print(df_result)

# visualization
obj.visualizations()

# push csv data to db
sess = define_session()
load_csv_dataset(sess)










