# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:32:59 2019

@author: thoma
"""

from chateau_weather import Chateau
from chateau_data import Chateau_data
from chateau_comb_new import Chateau_comb
from chateau_rating import Chateau_rating
import numpy as np
import ast
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
import json
import statistics
from geopy.geocoders import Nominatim
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier 
from sklearn.neural_network import MLPRegressor


#define our eomonth function
def eomonth(y, m):
    remainder = divmod(m,12)
    y_adj = remainder[0]
    m_adj = remainder[1] + 1
    given_day = datetime(y + y_adj, m_adj, 1)
    required_day = given_day - timedelta(days=1)
    return required_day

#unpack the dictionaries so the dates have the correct format
def dict_unpacker(sample_dict):
    dict_unpacked = {}
    for p_date, price in sample_dict.items():
         formattedas_date = datetime.strptime(p_date, "%Y-%m-%d")
         dict_unpacked[formattedas_date] = float(price)
    return dict_unpacked

# returns dict of average daily weather data aggregated by month
def seasonal_weather_dict(dict_sample):
    """returns dict of average daily weather data aggregated by month"""
    monthly_weather_dict = {}
    for p_date, precip in dict_sample.items():
        formattedas_date = p_date
        #datetime.strptime(p_date, "%Y-%m-%d")
        y = formattedas_date.year
        m = formattedas_date.month
        needed_day = eomonth(y, m)
        if needed_day in monthly_weather_dict.keys():
            x = monthly_weather_dict[needed_day][0] + float(precip)
            y = monthly_weather_dict[needed_day][1] + 1
            monthly_weather_dict[needed_day]  = [x, y]
        else:
            monthly_weather_dict[needed_day] = [float(precip), 1]
    
    monthly_weather_dict_av = {}
    for needed_day in monthly_weather_dict.keys():
        d = monthly_weather_dict[needed_day][0] / monthly_weather_dict[needed_day][1]
        monthly_weather_dict_av[needed_day] = d
    return monthly_weather_dict_av

#returns average seasonal weather dict
def average_seasonal_weather_dict(dict_sample):
    """returns average seasonal weather dictionary"""
    monthly_weather_dict = seasonal_weather_dict(dict_sample)
    average_seasonal_weather_dict = {}
    for p_date, precip in monthly_weather_dict.items():
        if p_date.month in average_seasonal_weather_dict.keys():
            x = average_seasonal_weather_dict[p_date.month][0] + float(precip)
            y = average_seasonal_weather_dict[p_date.month][1] + 1
            average_seasonal_weather_dict[p_date.month] = [x, y]
        else:
            average_seasonal_weather_dict[p_date.month] = [float(precip), 1]
    
    average_seasonal_weather_dict_final = {}
    for month, list_element in average_seasonal_weather_dict.items():
        d = (list_element[0] / list_element[1])
        average_seasonal_weather_dict_final[month] = d

    return average_seasonal_weather_dict_final

#returns dict of weather data aggregated by month for vintage year  
def vintage_monthly_weather_dict(dict_sample, vintage):
    """returns dict of weather data aggregated by month for vintage year"""
    monthly_weather_dict = seasonal_weather_dict(dict_sample)    
    vintage_monthly_weather_dict_final = {}
    for p_date, precip in monthly_weather_dict.items():
        if p_date.year == vintage:
            vintage_monthly_weather_dict_final[p_date] = precip
    return vintage_monthly_weather_dict_final

def all_monthly_weather_dict(dict_sample, chosen_month):
    """returns dict of weather data for chosen month for all years"""
    monthly_weather_dict = seasonal_weather_dict(dict_sample)    
    all_monthly_weather_dict_final = {}
    for p_date, precip in monthly_weather_dict.items():
        if p_date.month == int(chosen_month):
            all_monthly_weather_dict_final[p_date] = precip
    return all_monthly_weather_dict_final

def all_monthly_weather_dict_detail(dict_sample):
    """returns dict of mean, stdev for every month"""
    monthly_weather_dict = seasonal_weather_dict(dict_sample)    
    all_monthly_weather_dict = {}
    for chosen_month in range(1,13):
        new_list = []
        for p_date, precip in monthly_weather_dict.items():
            if p_date.month == int(chosen_month) and p_date > datetime(1970, 12, 31):
                new_list.append(precip)
        av = statistics.mean(new_list)
        sd = statistics.stdev(new_list)
        all_monthly_weather_dict[chosen_month] = [av, sd]
    return all_monthly_weather_dict


#------------------------------------------------------------------------

class Chateau_fundamentals():
    
    def __init__(self, address):
        """initialize attributes to define a stock"""
        self.address = address
    
    def chateau_profile(self, name, data=''):
        """Store a profile in the file so we do not repeat every action"""
        filename = (str(self.address) + "_fundamentals_profile.txt")
        #open as write - this takes care of the initial instance of the file
        # if we can read the profile read it, otherwise create an empty dict

        try:
            with open(filename) as f:
                contents = json.load(f)
            chateau_profile_dict = contents

        except FileNotFoundError:
            chateau_profile_dict = {}

        except ValueError:
            print("dictionary has a value error")
            chateau_profile_dict = {}
                 
        # if there is an existing entry:     
        if name in chateau_profile_dict.keys():
            if data:
                del chateau_profile_dict[name]
                chateau_profile_dict[name] = data
                # store the amended profile          
                with open(filename, 'w') as f:
                    json.dump(chateau_profile_dict,f)
                return chateau_profile_dict[name]
            else:
                return chateau_profile_dict[name]
        
        # if there isn't an existing entry
        else:
            if data:
                # create a new one if there is data
                chateau_profile_dict[name] = data
                # store the amended profile          
                with open(filename, 'w') as f:
                    json.dump(chateau_profile_dict,f)
                return chateau_profile_dict[name]

            else:
                # return nothing if there isn't
                return None

    def hemisphere_finder(self, update=''):
        """find the hemisphere of the vineyard"""
        def proceed_with_method():
            geolocator = Nominatim(user_agent="specify_your_app_name_here")
            location = geolocator.geocode(self.address)
            
            if location.latitude >= 0:
                hemisphere = 'N'
            elif location.latitude < 0:
                hemisphere = 'S'
            
            return hemisphere
        
        title = "hemisphere_finder"
        if update:
            data = proceed_with_method()
            Chateau_fundamentals(self.address).chateau_profile(title, data)
            print(str(title) + " updated")
            return Chateau_fundamentals(self.address).chateau_profile(title)

        elif Chateau_fundamentals(self.address).chateau_profile(title) == None:
            data = proceed_with_method()
            Chateau_fundamentals(self.address).chateau_profile(title, data)
            return Chateau_fundamentals(self.address).chateau_profile(title)

        else:
            return Chateau_fundamentals(self.address).chateau_profile(title) 
    
    
    def fundamental_dates(self, vintage, update=''):
        """returns the weather profile of the vintage vs average seasonality"""
       
        def proceed_with_method():
           
            weather_dict_p_raw = Chateau(self.address).weather_dict('p')
            weather_dict_v_raw = Chateau(self.address).weather_dict('v')
           
            weather_dict_p = dict_unpacker(weather_dict_p_raw)
            weather_dict_v = dict_unpacker(weather_dict_v_raw)

            #get the right start date depending on hemisphere
            hemisphere = Chateau_fundamentals(self.address).chateau_profile('hemisphere_finder')

            if hemisphere == 'N':
                start_month = 4
            elif hemisphere == 'S':
                start_month = 10
            else:
                print("Hemisphere location error")
            

            vintage_start_date = eomonth(vintage, start_month-1)
            
            #make a list of dates in the vintage
            vintage_dates = []
            
            #find the budbreak start date
            for w_date, temp in weather_dict_v.items():
                if w_date > vintage_start_date - timedelta(days=5) and w_date < vintage_start_date + timedelta(days = 365):
                    vintage_dates.append(w_date)

            bud_break_start_date = vintage_start_date
            bud_break_strike = 0

            for i in range(4,len(vintage_dates)-1):  #need the start date to have a mavg
                mavg_list = []
                for t in (0,4):
                    mavg_list.append(weather_dict_v[vintage_dates[i - t]])
                
                fdav = statistics.mean(mavg_list)
                #print(fdav)
            
                if fdav > 10 and bud_break_start_date == vintage_start_date:
                    bud_break_start_date = vintage_dates[i]
                
                if fdav < 1 and bud_break_start_date != vintage_start_date and vintage_dates[i] > bud_break_start_date and vintage_dates[i] < bud_break_start_date + timedelta(days = 80):
                    bud_break_strike = bud_break_strike + 1
            
            
            #find the flowering start date
            flower_start_date = bud_break_start_date
            flower_strike = 0
            
            for i in range(4,len(vintage_dates)-1):  #need the start date to have a mavg
                mavg_list = []
                for t in (0,4):
                    mavg_list.append(weather_dict_v[vintage_dates[i - t]])
                
                fdav = statistics.mean(mavg_list)
                #print(fdav)
            
                if fdav > 20 and bud_break_start_date == flower_start_date and vintage_dates[i] > bud_break_start_date + timedelta(days = 20):
                    flower_start_date = vintage_dates[i]
                
                if fdav < 15 and bud_break_start_date != flower_start_date and vintage_dates[i] > flower_start_date and vintage_dates[i] < flower_start_date + timedelta(days = 42):
                    flower_strike = flower_strike + 1            
            
            
            fruit_set_start_date = flower_start_date + timedelta(days=30)
            veraison_start_date = fruit_set_start_date + timedelta(days=45)
            #find the harvest start date
            harvest_start_date = veraison_start_date
            for i in range(4,len(vintage_dates)-1):  #need the start date to have a mavg
                mavg_list = []
                for t in (0,4):
                    mavg_list.append(weather_dict_v[vintage_dates[i - t]])
                
                fdav = statistics.mean(mavg_list)
                #print(fdav)
            
                if fdav <16 and veraison_start_date == harvest_start_date and vintage_dates[i] > veraison_start_date + timedelta(days = 10):
                    harvest_start_date = vintage_dates[i]

            names_list = ['bud_break',
                          'flower',
                          'fruit_set',
                          'veraison',
                          'harvest']
            
            start_dates_list = [bud_break_start_date, 
                                flower_start_date, 
                                fruit_set_start_date, 
                                veraison_start_date,
                                harvest_start_date]
            
            length_list = []
            def days_between(d1, d2):

                return abs((d2 - d1).days)
            
            for i in range(0,4):
                d = days_between(start_dates_list[i],start_dates_list[i+1])
                length_list.append(d)
            length_list.append(0)
            
            
            p_list, v_list = [], []
            
            for i in range(0,4):
                p_counter = 0
                for p_date, precip in weather_dict_p.items():
                    if p_date >= start_dates_list[i] and p_date < start_dates_list[i+1]:
                        p_counter = p_counter + precip
                p_list.append(p_counter)
            p_list.append(0)

            for i in range(0,4):
                v_counter = 0
                total = 0
                for v_date, temp in weather_dict_v.items():
                    if v_date >= start_dates_list[i] and v_date < start_dates_list[i+1]:
                        v_counter = v_counter + temp
                        total = total + 1
                if total ==0:
                    print("no data for " + str(vintage))
                    return None
                v_av = v_counter / total
                v_list.append(v_av)
            v_list.append(0)


            #print(names_list)
            #print(start_dates_list)
            #print(p_list)
            #print(v_list)
            
            fundamentals = {}
            for i in range(0,5):
                fundamentals[names_list[i]] = [str(start_dates_list[i]), length_list[i], p_list[i], v_list[i]]
            
            return fundamentals

        title = "fundamental_dates_"+str(vintage)
        if update:
            data = proceed_with_method()
            Chateau_fundamentals(self.address).chateau_profile(title, data)
            print(str(title) + " updated")
            return Chateau_fundamentals(self.address).chateau_profile(title)

        elif Chateau_fundamentals(self.address).chateau_profile(title) == None:
            data = proceed_with_method()
            Chateau_fundamentals(self.address).chateau_profile(title, data)
            return Chateau_fundamentals(self.address).chateau_profile(title)

        else:
            return Chateau_fundamentals(self.address).chateau_profile(title) 


    def fundamental_analysis_print(self, category, number):
        """analysis of vintage rule strikes vs price"""
        def proceed_with_method():

            price_dict_raw = Chateau_data(self.address).get_price_data()
            price_dict = dict_unpacker(price_dict_raw)
            
            x_values, y_values, z_values = [], [], []
            
            for p_date, price in price_dict.items():
                if p_date > datetime(1970, 12, 31):
                    y_values.append(price)
                    x_values.append(p_date)
            
            for p_date in x_values:
                vintage = p_date.year
                title = "fundamental_dates_"+str(vintage)
                values_dict = Chateau_fundamentals(self.address).chateau_profile(title) 
                z_values.append(values_dict[str(category)][number])
                
            #calculate best fit line
          
            
            x = z_values
            y = y_values
            z = np.polyfit(x, y, 2)
            p = np.poly1d(z)
            xp = np.linspace(min(x), max(x), 100) 
            
            #calculate correlation coefficient
            correl_y = p(x)
            #A = np.vstack([x, np.ones(len(x))]).T
            #m, c = np.linalg.lstsq(A, correl_y, rcond=None)[0]
            #print(m, c)
            R = np.corrcoef(y, correl_y)
            cor = R.item(1) #R is a 2x2 matrix so take the correct entry
            print("\nCorrelation coefficient: " + str(cor))
                       
            print("\nSuggested polynomial a*x^2 + bx + c has [a, b, c]: " + str(z))
    
                        
            #Size the output
            fig = plt.figure(dpi=128, figsize=(10,6))
            
            #Chart gridlines
            plt.grid(None, 'major', 'both')
            
            #Axis tick formats
            for tick in plt.gca().get_xticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
                tick.set_rotation('vertical')
            for tick in plt.gca().get_yticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
            
            #Axis labels and formats
            
            # axis 1
            color = 'tab:blue'
            plt.xlabel(str(category.title()), fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Price", color='black', fontsize =12)
            plt.scatter(z_values, y_values, color=color)
            plt.plot(xp, p(xp), color = 'red')
            plt.tick_params(axis='y', labelcolor=color)
            
                       
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " " + str(category.title())+ " Fundamentals:  ", fontsize = 14)
            
            #Show chart
            plt.show()
            
        proceed_with_method()

    def fundamental_regression(self):
        """analysis of vintage rule strikes vs price"""
        def proceed_with_method():

            price_dict_raw = Chateau_data(self.address).get_price_data()
            price_dict = dict_unpacker(price_dict_raw)
            
            x_values_train, y_values_train, z_values_train = [], [], []
            x_values_test, y_values_test, z_values_test = [], [], []
            
            for p_date, price in price_dict.items():
                if p_date > datetime(1970, 12, 31) and p_date <= datetime(2000, 12, 31):
                    y_values_train.append(price)
                    x_values_train.append(p_date)
                if p_date > datetime(2000, 12, 31):
                    y_values_test.append(price)
                    x_values_test.append(p_date)

            test_list = [['bud_break', 1],
                         ['bud_break', 2],
                         ['bud_break', 3],
                         ['flower', 1],
                         ['flower', 2],
                         ['flower', 3],
                         ['fruit_set', 1],
                         ['fruit_set', 2],
                         ['fruit_set', 3],
                         ['veraison', 1],
                         ['veraison', 2],
                         ['veraison', 3]]

            for p_date in x_values_train:
                vintage = p_date.year
                title = "fundamental_dates_"+str(vintage)
                values_dict = Chateau_fundamentals(self.address).chateau_profile(title) 
                z_values_list = []
                for i in range(0, len(test_list)-1):
                    z_values_list.append(values_dict[str(test_list[i][0])][test_list[i][1]])
                z_values_train.append(z_values_list)

            for p_date in x_values_test:
                vintage = p_date.year
                title = "fundamental_dates_"+str(vintage)
                values_dict = Chateau_fundamentals(self.address).chateau_profile(title) 
                z_values_list = []
                for i in range(0, len(test_list)-1):
                    z_values_list.append(values_dict[str(test_list[i][0])][test_list[i][1]])
                z_values_test.append(z_values_list)

            scaler = StandardScaler()  
            # Don't cheat - fit only on training data
            scaler.fit(z_values_train)  
            X_train = scaler.transform(z_values_train)  
            # apply same transformation to test data
            X_test = scaler.transform(z_values_train + z_values_test)
            
            X = X_train
            y = y_values_train
            clf = MLPRegressor(solver='lbfgs', alpha=1e-5,
                                hidden_layer_sizes=(5, 2), random_state=1)

            clf.fit(X, y)                         
            MLPRegressor(activation='relu', alpha=1e-05, batch_size='auto',
                          beta_1=0.9, beta_2=0.999, early_stopping=False,
                          epsilon=1e-08, hidden_layer_sizes=(5, 2),
                          learning_rate='constant', learning_rate_init=0.001,
                          max_iter=200, momentum=0.9, n_iter_no_change=10,
                          nesterovs_momentum=True, power_t=0.5, random_state=1,
                          shuffle=True, solver='lbfgs', tol=0.0001,
                          validation_fraction=0.1, verbose=False, warm_start=False)
            
            results = clf.predict(X_test)
            #print(results)
            #print(str(results).replace(' ',', ').replace(' ,',''))
            
            y_values_pred_raw = str(results).replace(' ',', ').replace(' ,','')
            
            y_values_pred = ast.literal_eval(y_values_pred_raw)
            #for i in range(0,len(y_values_pred_raw)-1):
                #y_values_pred.append(float(y_values_pred_raw[i]))
            
            print(y_values_pred)
            
            
                

            print([coef.shape for coef in clf.coefs_])

            #print(clf.predict_proba(z_values_test))  


            # Create linear regression object
            ##regr = linear_model.LinearRegression()
            
            # Train the model using the training sets
            #regr.fit(z_values_train, y_values_train)
            
            # Make predictions using the testing set
            #y_values_pred = regr.predict(z_values_test)
            
            # The coefficients
            #print('Coefficients: \n', regr.coef_)
            # The mean squared error
            #print("Mean squared error: %.2f"
                 ## % mean_squared_error(y_values_test, y_values_pred))
            # Explained variance score: 1 is perfect prediction
            ##print('R2 score: %.2f' % r2_score(y_values_test, y_values_pred))
           # print('R2 score: %.2f' % r2_score(y_values_test, y_values_pred))            

                        #Size the output
            fig = plt.figure(dpi=128, figsize=(10,6))
            
            #Chart gridlines
            plt.grid(None, 'major', 'both')
            
            #Axis tick formats
            for tick in plt.gca().get_xticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
                tick.set_rotation('vertical')
            for tick in plt.gca().get_yticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
            
            #Axis labels and formats
            
            # axis 1
            color = 'tab:blue'
            plt.xlabel("Date", fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Price", color='black', fontsize =12)
            plt.bar(x_values_train + x_values_test, y_values_train + y_values_test, facecolor='none', edgecolor='blue',)
            plt.scatter(x_values_train + x_values_test, y_values_pred, color='red', linestyle ='dashed')
            plt.tick_params(axis='y', labelcolor=color)
            
            #ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
            
            #axis 2
            #color = 'tab:red'
            #ax2.set_ylabel("Price", color='black', fontsize=12)  # we already handled the x-label with ax1
            #ax2.plot(x_values, y_values, color=color)
            #ax2.scatter(x_values, z_values, color=color, linestyle='dashed')
            #ax2.tick_params(axis='y', labelcolor=color)
            
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " actual px vs forecast", fontsize = 14)
            
            #Show chart
            plt.show()
            



        proceed_with_method()

    def fundamental_regression_rating(self):
        """analysis of vintage rule strikes vs price"""
        def proceed_with_method():

            price_dict_raw = Chateau_rating(self.address).get_rating_data()
            #Chateau_data(self.address).get_price_data()
            price_dict = dict_unpacker(price_dict_raw)
            
            x_values_train, y_values_train, z_values_train = [], [], []
            x_values_test, y_values_test, z_values_test = [], [], []
            
            for p_date, price in price_dict.items():
                if p_date > datetime(1970, 12, 31) and p_date <= datetime(2000, 12, 31):
                    y_values_train.append(price)
                    x_values_train.append(p_date)
                if p_date > datetime(2000, 12, 31):
                    y_values_test.append(price)
                    x_values_test.append(p_date)

            test_list = [#['bud_break', 1],
                         #['bud_break', 2],
                         #['bud_break', 3],
                         #['flower', 1],
                         #['flower', 2],
                         #['flower', 3],
                         #['fruit_set', 1],
                         #['fruit_set', 2],
                         #['fruit_set', 3],
                         ['veraison', 1],
                         #['veraison', 2],
                         #['veraison', 3]
                         ]

            
            for p_date in x_values_train:
                vintage = p_date.year
                title = "fundamental_dates_"+str(vintage)
                values_dict = Chateau_fundamentals(self.address).chateau_profile(title) 
                z_values_list = []
                for i in range(0, 1): #len(test_list)-1
                    z_values_list.append(values_dict[str(test_list[i][0])][test_list[i][1]])
                z_values_train.append(z_values_list)
            print(z_values_train)
            for p_date in x_values_test:
                vintage = p_date.year
                try:
                    title = "fundamental_dates_"+str(vintage)
                    values_dict = Chateau_fundamentals(self.address).chateau_profile(title)
                    z_values_list = []
                    for i in range(0, 1): #len(test_list)-1
                        z_values_list.append(values_dict[str(test_list[i][0])][test_list[i][1]])
                    z_values_test.append(z_values_list)
                except Exception:
                    z_values_test.append('')
            
            for i in range(0, len(x_values_test)-1):
                if z_values_test[i] == '':
                    x_values_test.pop(i)
                    y_values_test.pop(i)
                    z_values_test.pop(i)

            # Create linear regression object
            regr = linear_model.LinearRegression()
            
            # Train the model using the training sets
            regr.fit(z_values_train, y_values_train)
            
            # Make predictions using the testing set
            y_values_pred = regr.predict(z_values_test)
            correl_y = regr.predict(z_values_train + z_values_test)
            
            # The coefficients
            print('Coefficients: \n', regr.coef_)
            # The mean squared error
            print("Mean squared error: %.2f"
                  % mean_squared_error(y_values_test, y_values_pred))
            # Explained variance score: 1 is perfect prediction
            print('R2 score: %.2f' % r2_score(y_values_test, y_values_pred))
            
            #Size the output
            fig = plt.figure(dpi=128, figsize=(10,6))
            
            #Chart gridlines
            plt.grid(None, 'major', 'both')
            
            #Axis tick formats
            for tick in plt.gca().get_xticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
                tick.set_rotation('vertical')
            for tick in plt.gca().get_yticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
            
            #Axis labels and formats
            
            # axis 1
            color = 'tab:blue'
            plt.xlabel("Date", fontsize =12)
            plt.ylabel("Price", color='black', fontsize =12)
            plt.bar(x_values_train + x_values_test, y_values_train + y_values_test, facecolor='none', edgecolor='blue',)
            plt.scatter(x_values_train + x_values_test, correl_y, color='red', linestyle ='dashed')
            plt.tick_params(axis='y', labelcolor=color)
            plt.ylim((85,110))
            
            #ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
            
            #axis 2
            #color = 'tab:red'
            #ax2.set_ylabel("Price", color='black', fontsize=12)  # we already handled the x-label with ax1
            #ax2.plot(x_values, y_values, color=color)
            #ax2.scatter(x_values, z_values, color=color, linestyle='dashed')
            #ax2.tick_params(axis='y', labelcolor=color)
            
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " actual px vs forecast", fontsize = 14)
            
            #Show chart
            plt.show()




        proceed_with_method()

    def seasonality_correlation(self, update=''):
        """returns the weather profile of the vintage vs average seasonality"""
       
        def proceed_with_method():
           
            weather_dict_p_raw = Chateau(self.address).weather_dict('p')
            weather_dict_v_raw = Chateau(self.address).weather_dict('v')

           
            weather_dict_p = dict_unpacker(weather_dict_p_raw)
            weather_dict_v = dict_unpacker(weather_dict_v_raw)
            
            rating_dict_raw = Chateau_rating(self.address).get_rating_data()
            rating_dict = dict_unpacker(rating_dict_raw)
            
            seasonal_weather_dict_p = average_seasonal_weather_dict(weather_dict_p)
            seasonal_weather_dict_v = average_seasonal_weather_dict(weather_dict_v)

            x_values_train, x_values_test = [], []
            y_values_train, y_values_test = [], []
            t_values_train, t_values_test = [], []
            
            for r_date, rating in rating_dict.items():
                if r_date > datetime(1970, 12, 31) and r_date <= datetime(2008,12,31):
                    vintage = r_date.year
            
                    monthly_weather_dict_p = vintage_monthly_weather_dict(weather_dict_p, vintage)
                    monthly_weather_dict_v = vintage_monthly_weather_dict(weather_dict_v, vintage)

                    # start chart
                    x_values, y_values, z_values = [], [], []
                    #sy_values, sz_values = [], []
                    
                    for key in monthly_weather_dict_p.keys():
                        x_date = key
                        #y_values.append(float(str(monthly_weather_dict_p[key])))
                        #z_values.append(monthly_weather_dict_v[x_date])
                        y_values.append(float(str(monthly_weather_dict_p[key]))-float(str(seasonal_weather_dict_p[key.month])))
                        z_values.append(monthly_weather_dict_v[x_date]-seasonal_weather_dict_v[x_date.month])
                        #sy_values.append(float(str(seasonal_weather_dict_p[key.month])))
                        #sz_values.append(seasonal_weather_dict_v[x_date.month])
                    t_values_train.append(r_date)
                    y_values_train.append(rating)
                    x_values_train.append(y_values + z_values)
                    #z_values_train.append(z_values)

                if r_date > datetime(2008,12,31) and r_date in weather_dict_p.keys() and r_date in weather_dict_v.keys():
                    vintage = r_date.year
            
                    monthly_weather_dict_p = vintage_monthly_weather_dict(weather_dict_p, vintage)
                    monthly_weather_dict_v = vintage_monthly_weather_dict(weather_dict_v, vintage)

                    # start chart
                    x_values, y_values, z_values = [], [], []
                    #sy_values, sz_values = [], []
                    
                    for key in monthly_weather_dict_p.keys():
                        x_date = key
                        #y_values.append(float(str(monthly_weather_dict_p[key])))
                        #z_values.append(monthly_weather_dict_v[x_date])
                        y_values.append(float(str(monthly_weather_dict_p[key]))-float(str(seasonal_weather_dict_p[key.month])))
                        z_values.append(monthly_weather_dict_v[x_date]-seasonal_weather_dict_v[x_date.month])
                        #sy_values.append(float(str(seasonal_weather_dict_p[key.month])))
                        #sz_values.append(seasonal_weather_dict_v[x_date.month])

                    t_values_test.append(r_date)
                    y_values_test.append(rating)
                    x_values_test.append(y_values + z_values)
            
            print(t_values_train + t_values_test)
            
            # Create linear regression object
            regr = linear_model.LinearRegression()
            
            # Train the model using the training sets
            regr.fit(x_values_train, y_values_train)
            
            # Make predictions using the testing set
            y_values_pred = regr.predict(x_values_test)
            correl_y = regr.predict(x_values_train + x_values_test)
            
            # The coefficients
            print('Coefficients: \n', regr.coef_)
            # The mean squared error
            print("Mean squared error: %.2f"
                  % mean_squared_error(y_values_test, y_values_pred))
            # Explained variance score: 1 is perfect prediction
            print('R2 score: %.2f' % r2_score(y_values_test, y_values_pred))
            
            #Size the output
            fig = plt.figure(dpi=128, figsize=(10,6))
            
            #Chart gridlines
            plt.grid(None, 'major', 'both')
            
            #Axis tick formats
            for tick in plt.gca().get_xticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
                tick.set_rotation('vertical')
            for tick in plt.gca().get_yticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
            
            #Axis labels and formats
            
            # axis 1
            color = 'tab:blue'
            plt.xlabel("Date", fontsize =12)
            plt.ylabel("Price", color='black', fontsize =12)
            plt.bar(t_values_train + t_values_test, y_values_train + y_values_test, facecolor='none', edgecolor='blue',)
            plt.scatter(t_values_train + t_values_test, correl_y, color='red', linestyle ='dashed')
            plt.tick_params(axis='y', labelcolor=color)
            plt.ylim((70,110))
            
            #ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
            
            #axis 2
            #color = 'tab:red'
            #ax2.set_ylabel("Price", color='black', fontsize=12)  # we already handled the x-label with ax1
            #ax2.plot(x_values, y_values, color=color)
            #ax2.scatter(x_values, z_values, color=color, linestyle='dashed')
            #ax2.tick_params(axis='y', labelcolor=color)
            
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " actual px vs forecast", fontsize = 14)
            
            #Show chart
            plt.show()

        proceed_with_method() 

    def machine_learning(self):
        """analysis of vintage rule strikes vs price"""
        def proceed_with_method():

            price_dict_raw = Chateau_data(self.address).get_price_data()
            price_dict = dict_unpacker(price_dict_raw)
            
            weather_dict_p_raw = Chateau(self.address).weather_dict('p')
            weather_dict_v_raw = Chateau(self.address).weather_dict('v')

           
            weather_dict_p = dict_unpacker(weather_dict_p_raw)
            weather_dict_v = dict_unpacker(weather_dict_v_raw)
            
            

            
            # start chart
            x_values, y_values, z_values = [], [], []
            p_values_train, p_values_test = [], []
            x_values_train, x_values_test = [], []
            y_values_train, y_values_test = [], []
            z_values_train, z_values_test = [], []
        
            for p_date, price in price_dict.items():

                vintage = p_date.year
                monthly_weather_dict_p = vintage_monthly_weather_dict(weather_dict_p, vintage)
                monthly_weather_dict_v = vintage_monthly_weather_dict(weather_dict_v, vintage)
                  
                if p_date > datetime(1970, 12, 31) and p_date <= datetime(2000, 12, 31):
                    p_values_train.append(price)
                    
                    x_vector_train = []
                    y_vector_train = []
                    z_vector_train = []
                                        
                    for key in monthly_weather_dict_p.keys():
                        x_date = key
                        x_vector_train.append(key)
                        y_vector_train.append(float(str(monthly_weather_dict_p[key])))
                        y_vector_train.append(monthly_weather_dict_v[x_date])
                    
                    x_values_train.append(x_vector_train)
                    y_values_train.append(y_vector_train)
                    z_values_train.append(z_vector_train)
                    
                if p_date > datetime(2000, 12, 31):
                    p_values_test.append(price)
                    
                    x_vector_test = []
                    y_vector_test = []
                    z_vector_test = []
                                        
                    for key in monthly_weather_dict_p.keys():
                        x_date = key
                        x_vector_test.append(key)
                        y_vector_test.append(float(str(monthly_weather_dict_p[key])))
                        z_vector_test.append(monthly_weather_dict_v[x_date])
                    
                    x_values_test.append(x_vector_test)
                    y_values_test.append(y_vector_test)
                    y_values_test.append(z_vector_test)                    
                    
            x_train = y_values_train
            x_test = y_values_test
            print(x_train)
            print(p_values_train)
            
            scaler = StandardScaler()  
            # Don't cheat - fit only on training data
            scaler.fit(x_train)  
            X_train = scaler.transform(x_train)  
            # apply same transformation to test data
            X_test = scaler.transform(x_test)
            
            X = X_train
            y = p_values_train
            clf = MLPRegressor(solver='lbfgs', alpha=1e-5,
                                hidden_layer_sizes=(5, 2), random_state=1)

            clf.fit(X, y)                         
            MLPRegressor(activation='relu', alpha=1e-05, batch_size='auto',
                          beta_1=0.9, beta_2=0.999, early_stopping=False,
                          epsilon=1e-08, hidden_layer_sizes=(5, 2),
                          learning_rate='constant', learning_rate_init=0.001,
                          max_iter=200, momentum=0.9, n_iter_no_change=10,
                          nesterovs_momentum=True, power_t=0.5, random_state=1,
                          shuffle=True, solver='lbfgs', tol=0.0001,
                          validation_fraction=0.1, verbose=False, warm_start=False)
            
            results = clf.predict(X_test)
            print(results)
            #print(str(results).replace(' ',', ').replace(' ,',''))
            
            y_values_pred_raw = str(results).replace(' ',', ').replace(' ,','')
            
            y_values_pred = ast.literal_eval(y_values_pred_raw)
            #for i in range(0,len(y_values_pred_raw)-1):
                #y_values_pred.append(float(y_values_pred_raw[i]))
            
            #print(y_values_pred)
            
            
                

            print([coef.shape for coef in clf.coefs_])

            #print(clf.predict_proba(z_values_test))  


            # Create linear regression object
            ##regr = linear_model.LinearRegression()
            
            # Train the model using the training sets
            #regr.fit(z_values_train, y_values_train)
            
            # Make predictions using the testing set
            #y_values_pred = regr.predict(z_values_test)
            
            # The coefficients
            #print('Coefficients: \n', regr.coef_)
            # The mean squared error
            #print("Mean squared error: %.2f"
            #     % mean_squared_error(p_values_test, y_values_pred))
            #Explained variance score: 1 is perfect prediction
            #print('R2 score: %.2f' % r2_score(p_values_test, y_values_pred))
           # print('R2 score: %.2f' % r2_score(y_values_test, y_values_pred))            

                        #Size the output
            fig = plt.figure(dpi=128, figsize=(10,6))
            
            #Chart gridlines
            plt.grid(None, 'major', 'both')
            
            #Axis tick formats
            for tick in plt.gca().get_xticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
                tick.set_rotation('vertical')
            for tick in plt.gca().get_yticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
            
            #Axis labels and formats
            
            # axis 1
            color = 'tab:blue'
            plt.xlabel("Date", fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Price", color='black', fontsize =12)
            plt.bar(x_values_train + x_values_test, p_values_train + p_values_test, facecolor='none', edgecolor='blue',)
            plt.scatter(x_values_train + x_values_test, y_values_pred, color='red', linestyle ='dashed')
            plt.tick_params(axis='y', labelcolor=color)
            
            #ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
            
            #axis 2
            #color = 'tab:red'
            #ax2.set_ylabel("Price", color='black', fontsize=12)  # we already handled the x-label with ax1
            #ax2.plot(x_values, y_values, color=color)
            #ax2.scatter(x_values, z_values, color=color, linestyle='dashed')
            #ax2.tick_params(axis='y', labelcolor=color)
            
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " actual px vs forecast", fontsize = 14)
            
            #Show chart
            plt.show()


        proceed_with_method()


#Chateau_fundamentals("Chateau Margaux").hemisphere_finder()  
#Chateau_data("Chateau Margaux").print_wine_price(1940)   
#Chateau_comb("Chateau Margaux").vintage_patterns(2013)
#for i in range(1940, 1970):
    #Chateau_fundamentals("Chateau Margaux").fundamental_dates(i, 'update')
#Chateau_fundamentals("Chateau Margaux").fundamental_dates(2017, 'update')
#1 length, 2 precip, 3 temp
#Chateau_fundamentals("Chateau Margaux").fundamental_analysis('bud_break', 3)
#Chateau_fundamentals("Chateau Margaux").fundamental_analysis('flower', 2)
#Chateau_fundamentals("Chateau Margaux").fundamental_analysis('flower', 3)
#Chateau_fundamentals("Chateau Margaux").fundamental_analysis('fruit_set', 2)
#Chateau_fundamentals("Chateau Margaux").fundamental_analysis('fruit_set', 3)
#Chateau_fundamentals("Chateau Margaux").fundamental_analysis('veraison', 2)
#Chateau_fundamentals("Chateau Margaux").fundamental_analysis('veraison', 3)
#Chateau_fundamentals("Chateau Margaux").fundamental_analysis('flower', 1)
#Chateau_fundamentals("Chateau Margaux").fundamental_analysis('fruit_set', 1)
#Chateau_fundamentals("Chateau Margaux").machine_learning()
#Chateau_fundamentals("Chateau Margaux").fundamental_regression_rating()




   
