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


x = df[['year', 'km']]
y = df['price']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

LR = LinearRegression()

LR.fit(x_train,y_train)

y_prediction = LR.predict(x_test)

df2 = pd.DataFrame({**x_test, 'Actual': y_test, 'Predicted': y_prediction})
total = 0
right = 0
print(df2)
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_prediction))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_prediction))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_prediction)))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['year'], df['km'], df['price'], marker='.', color='blue', alpha=0.1, zorder=-1)
ax.scatter(2018, 40000, 1640, color='red', s=500,  zorder=1)
ax.plot(np.full(17, 2018), np.arange(10000, 180000, step=10000), np.full(17, 1640))
ax.plot(np.arange(2005, 2022), np.full(17, 40000), np.full(17, 1640))
ax.plot(np.full(17, 2018), np.full(17, 40000), np.arange(0, 2550, step=150))
ax.set_xlabel("Year")
ax.set_ylabel("Mileage")
ax.set_zlabel("Price")

coefs = LR.coef_
intercept = LR.intercept_
xs = np.tile(np.arange(2005, 2022), (17,1))
ys = np.tile(np.arange(10000, 180000, step=10000), (17,1)).T
zs = xs*coefs[0]+ys*coefs[1]+intercept
print("Equation: y = {:.2f} + {:.2f}x1 + {:.2f}x2".format(intercept, coefs[0],
                                                          coefs[1]))
ax.plot_surface(xs,ys,zs, alpha=0.3)
ax.view_init(azim=-130, elev=30)

plt.show()
