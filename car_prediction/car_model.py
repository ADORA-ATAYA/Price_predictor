from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import pymysql as mysql
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import svm


def show(request):
    render(request, "predictor.html",{'msg':'0 rs.'})
    symbol = request.POST.get('symbol',False)
    fuel = request.POST.get('fuel',False)
    e_size = request.POST.get('e-size',False)
    b_ratio = request.POST.get('b-ratio',False)
    stroke = request.POST.get('stroke',False)
    c_ratio = request.POST.get('c-ratio',False)
    h_power = request.POST.get('h-power',False)
    rpm = request.POST.get('rpm',False)
    mpg = request.POST.get('mpg',False)
    h_mpg = request.POST.get('h-mpg',False)
    try:
        dbe = mysql.connect(host="localhost", port=3306, user="root", password='9425starK@', db='cars')
        cmd = dbe.cursor()
        q = "insert into carsdata(Symboling,fueltype,enginesize,bore_ratio,stroke,c_ratio,horse_power,peak_rpm,city_mpg,highway_mpg) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')".format(symbol,fuel,e_size,b_ratio,stroke,c_ratio,h_power,rpm,mpg,h_mpg)
        cmd.execute(q)
        dbe.commit()
        dbe.close()


        car_data = pd.read_csv('E:/car_prediction/car_prediction/car_data.csv', index_col='car_ID')
        data = car_data.copy(deep=True)
        col_drop = ['wheelbase', 'carlength', 'carwidth', 'carheight', 'curbweight', 'enginelocation']
        data = data.drop(columns=col_drop)
        data['fueltype'] = data['fueltype'].map({'gas': 0, 'diesel': 1})
        main_data = data.select_dtypes(exclude=[object])
        x = main_data.drop(columns=['price'], axis=1).values
        y = main_data['price'].values
        c = []
        for i in y:
            c.append(int(i))
        cls = svm.SVC(kernel='linear', C=1)
        x_train, x_test, y_train, y_test = train_test_split(x, c, test_size=0.3, random_state=1)
        train_x = np.array(x_train).reshape(-1, 1)
        test_x = np.array(x_test).reshape(-1, 1)
        train_y = np.array(y_train).reshape(-1, 1)
        test_y = np.array(y_test).reshape(-1, 1)
        cls.fit(x_train, y_train)
        ans = cls.predict(x_test)
        p = np.array([symbol,fuel,e_size,b_ratio,stroke,c_ratio,h_power,rpm,mpg,h_mpg])
        pred_value=cls.predict([p])
        x=str(pred_value[0])+' rs.'
        return render(request,"predictor.html",{'msg':x})
    except Exception as e:
        print(e)
        return render(request,"predictor.html",{'msg':''})