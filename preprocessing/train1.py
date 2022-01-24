# Copyright 2021 Moonsik Park

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

df = pd.read_csv('normalized.csv')



for i in range(0, 6, 1):
    df_filtered = df[df['gen'] == i]
    x = df_filtered.drop(["price", "no"], axis=1)
    y = df_filtered['price']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 42)

    LR = LinearRegression()
    LR.fit(x_train,y_train)

    y_prediction = LR.predict(x_test)
    df2 = pd.DataFrame({**x_test, 'Actual': y_test, 'Predicted': y_prediction})
    
    print(f"Gen {i} 테스트 결과")
    print(f"data size: {len(df_filtered)}")
    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_prediction))
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_prediction))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_prediction)))
