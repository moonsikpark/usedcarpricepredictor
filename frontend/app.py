# Copyright 2021 Moonsik Park

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt
from io import BytesIO

TEST_SIZE = 0.3


df = pd.read_csv('normalized.csv')

x = df.drop(["price"], axis=1)
#x = df.drop(["price"], axis=1)
y = df['price']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = TEST_SIZE, random_state = 42)

LR = LinearRegression()

LR.fit(x_train,y_train)

y_prediction = LR.predict(x_test)

df2 = pd.DataFrame({**x_test, 'Actual': y_test, 'Predicted': y_prediction})

mean_absolute_error = metrics.mean_absolute_error(y_test, y_prediction)
mean_squared_error = metrics.mean_squared_error(y_test, y_prediction)
root_mean_squared_error = np.sqrt(metrics.mean_squared_error(y_test, y_prediction))


from flask import Flask, render_template, request, Response
from urllib import parse
from scrape import scrape

App = Flask(__name__)

@App.route('/')
def index():
    return render_template('main.html', title="ABC")

@App.route('/metrics')
def met():
    return {'mean_absolute_error': mean_absolute_error, 'mean_squared_error': mean_squared_error, "root_mean_squared_error": root_mean_squared_error}

@App.route('/encar_get_data')
def eva():
    url = request.args.get('url')
    car_id = parse.parse_qs(parse.urlparse(url).query)['carid'][0]
    result = scrape(car_id=car_id)
    d = pd.DataFrame.from_dict(result["traindata"], orient='index').T.drop("price", axis=1)
    prediction = LR.predict(d)[0]
    result["displaydata"]["prediction"] = int(prediction)
    result["displaydata"]["errorrate"] = int(abs(result["traindata"]["price"] - prediction))
    result["displaydata"]["errorratepercent"] = int(abs(result["traindata"]["price"] - prediction)/result["traindata"]["price"]*100)
    return result["displaydata"]

@App.route('/plot.png')
def plot_png():
    km = request.args.get('km')
    year = request.args.get('year')
    price = request.args.get('price')
    output = create_figure(km, year, price)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure(km=None, year=None, price=None):
    x = df[['year', 'km']]
    y = df['price']
    LR_fig = LinearRegression()
    LR_fig.fit(x,y)
    out = BytesIO()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df['year'], df['km'], df['price'], marker='.', color='blue', alpha=0.1, zorder=-1)
    ax.set_xlabel("Year")
    ax.set_ylabel("Mileage")
    ax.set_zlabel("Price")

    coefs = LR_fig.coef_
    intercept = LR_fig.intercept_
    xs = np.tile(np.arange(2005, 2022), (17,1))
    ys = np.tile(np.arange(10000, 180000, step=10000), (17,1)).T
    zs = xs*coefs[0]+ys*coefs[1]+intercept
    ax.plot_surface(xs,ys,zs, alpha=0.3)

    if km:
        km = int(km)
        price = int(price)
        year = int(year)
        ax.scatter(year, km, price, color='red', s=500,  zorder=1)
        ax.plot(np.full(17, year), np.arange(10000, 180000, step=10000), np.full(17, price))
        ax.plot(np.arange(2005, 2022), np.full(17, km), np.full(17, price))
        ax.plot(np.full(17, year), np.full(17, km), np.arange(0, 2550, step=150))
    
    ax.view_init(azim=-130, elev=30)
    fig.savefig(out, format="png")

    return out





