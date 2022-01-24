# Copyright 2021 Moonsik Park

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

df = pd.read_csv('normalized.csv')

df_original = df.copy()

for i in range(1, 100, 1):
    train, test = train_test_split(df, test_size = 0.01*i, random_state = 42)
    f = open(f"divide/ex{i}.csv", "w")
    f.write(test.to_csv())
    f.close()
