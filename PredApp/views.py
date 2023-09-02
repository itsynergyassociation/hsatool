from PredApp.models import PredictModel, TMRTParams, PMVParams, PETParams
from django.shortcuts import render, redirect
from .forms import PredictForm, TMRTForm, PMVForm, PETForm
from django.views.generic import View
from django.conf import settings
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from django.contrib.auth.models import User
import numpy as np
import pandas as pd
import keras
import os
import glob

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from django.core.cache import cache

def load_keras_model():
    print("Keras model loading.......")
    model_name = 'simul_model.h5'
    loaded_model = keras.models.load_model(os.path.join(settings.MODEL_ROOT, model_name))
    print("Model loaded !!")
    return loaded_model


simulations = pd.DataFrame()
for f in glob.glob("Dataset/*.xlsx"):
    df = pd.read_excel(f, parse_dates=['time'])
    simulations = pd.concat([simulations, df], ignore_index=True)

simulations['time'] = pd.to_datetime(simulations['time'], errors='coerce')
simulations['time'] = pd.Index(simulations['time'])
simulations = simulations.set_index("time")
simulations.drop('Unnamed: 7', inplace=True, axis=1)
simulations.drop('Thermal radiation', inplace=True, axis=1)
simulations = simulations.drop(simulations.index[0])
values = simulations.values
X = values[:, 0:5]
Y = values[:, 5:8]

# Split Data to Train and Test
X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=0.3, random_state=42)
X_scaler = MinMaxScaler()
X_train_scaled = X_scaler.fit_transform(X_Train)
X_test_scaled = X_scaler.transform(X_Test)
Y_scaler = MinMaxScaler()
Y_train_scaled = Y_scaler.fit_transform(Y_Train)
Y_test_scaled = Y_scaler.transform(Y_Test)

def home(request):
    return render(request, 'PredApp/home.html')

class Predictions(View):
    def get(self, *args, **kwargs):
        form = PredictForm()
        history = PredictModel.objects.all()

        context = {
            'form': form,
            'history': history,
        }

        return render(self.request, 'PredApp/predictions.html', context)
    
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            tmrtUser = TMRTParams.objects.filter(user=self.request.user).last()
            pmvUser = PMVParams.objects.filter(user=self.request.user).last()
            petUser = PETParams.objects.filter(user=self.request.user).last()
            form = PredictForm(self.request.POST)
            loaded_model = cache.get('keras_model')
            if loaded_model is None:
                loaded_model = load_keras_model()
                cache.set('keras_model', loaded_model, timeout=None)
            
            if form.is_valid():
                Global_radiation = form.cleaned_data.get('Global_radiation')
                Surface_temperature = form.cleaned_data.get('Surface_temperature')
                Air_temperature = form.cleaned_data.get('Air_temperature')
                Relative_Humidity = form.cleaned_data.get('Relative_Humidity')
                Wind_speed = form.cleaned_data.get('Wind_speed')
                x_input = np.array([[
                    float(Global_radiation), float(Surface_temperature),
                    float(Air_temperature), float(Relative_Humidity),
                    float(Wind_speed)
                ]])
                x_input = X_scaler.transform(x_input)
                x_input = x_input.reshape((-1, 1, 5))
                yhat = loaded_model.predict(x_input, verbose=0)
                yhat = yhat.reshape((yhat.shape[0], 3))
                yhat = Y_scaler.inverse_transform(yhat)
                result = yhat
                temper = PredictModel(
                    Global_radiation=Global_radiation,
                    # Thermal_radiation=Thermal_radiation,
                    Surface_temperature=Surface_temperature,
                    Air_temperature=Air_temperature,
                    Relative_Humidity=Relative_Humidity,
                    Wind_speed=Wind_speed,
                    Tmrt=round(result[:, 0][0], 4),
                    PMV=round(result[:, 1][0], 4),
                    PET=round(result[:, 2][0], 4),
                )

                color1 = ""
                if temper.PMV >= pmvUser.hot:
                    color1 = "#fd552c"
                elif pmvUser.warm <= temper.PMV < pmvUser.hot:
                    color1 = "#f97555"
                elif pmvUser.slwarm <= temper.PMV < pmvUser.warm:
                    color1 = "#fb937a"
                elif pmvUser.neutral < temper.PMV < pmvUser.slwarm:
                    color1 = "#cef4fa"
                elif pmvUser.slcool < temper.PMV < pmvUser.neutral:
                    color1 = "#10f4d0"
                elif pmvUser.cool < temper.PMV <= pmvUser.slcool:
                    color1 = "#28cbee"
                elif pmvUser.cold < temper.PMV <= pmvUser.cool:
                    color1 = "#76a0e8"
                elif temper.PMV <= pmvUser.cold:
                    color1 = "#4582eb"

                temper.PMVColor = color1

                color2 = ""
                if temper.PET < petUser.vcold:
                    color2 = "#4582eb"
                elif petUser.vcold <= temper.PET < petUser.cold:
                    color2 = "#6997e7"
                elif petUser.cold <= temper.PET < petUser.cool:
                    color2 = "#8cc6f0"
                elif petUser.cool <= temper.PET < petUser.slcool:
                    color2 = "#69dfe7"
                elif petUser.slcool <= temper.PET < petUser.comfort:
                    color2 = "#cef4fa"
                elif petUser.comfort <= temper.PET < petUser.slwarm:
                    color2 = "#fb937a"
                elif petUser.slwarm <= temper.PET < petUser.warm:
                    color2 = "#f97555"
                elif petUser.warm <= temper.PET < petUser.hot:
                    color2 = "#fd552c"
                elif temper.PET >= petUser.vhot:
                    color2 = "#e01607"

                temper.PETColor = color2

                color3 = ""
                if temper.Tmrt < tmrtUser.vlow:
                    color3 = "#fbf7b2"
                elif tmrtUser.vlow <= temper.Tmrt < tmrtUser.low:
                    color3 = "#f8f284"
                elif tmrtUser.low <= temper.Tmrt < tmrtUser.medium:
                    color3 = "#f3ea52"
                elif tmrtUser.medium <= temper.Tmrt < tmrtUser.high:
                    color3 = "#f8ec17"
                elif temper.Tmrt >= tmrtUser.vhigh:
                    color3 = "#edba04"

                temper.TmrtColor = color3

                temper.save()

                context = {
                    'Tmrt': temper.Tmrt,
                    'PMV': temper.PMV,
                    'PET': temper.PET,

                    'form': form
                }

                return render(self.request, "PredApp/predictions.html", context)
            else:
                return redirect('PredApp:prediction')


class History(View):
    def get(self, *args, **kwargs):
        histories = PredictModel.objects.all()

        context = {
            'histories': histories,
        }

        return render(self.request, 'PredApp/history.html', context)


class Settings(View):
    def get(self, *args, **kwargs):
        form1 = TMRTForm()
        form2 = PMVForm()
        form3 = PETForm()

        context = {
            'form1': form1,
            'form2': form2,
            'form3': form3
        }

        return render(self.request, "PredApp/params.html", context)

    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            form1 = TMRTForm(self.request.POST)
            form2 = PMVForm(self.request.POST)
            form3 = PETForm(self.request.POST)

            if form1.is_valid():
                vlow = form1.cleaned_data.get('vlow')
                low = form1.cleaned_data.get('low')
                medium = form1.cleaned_data.get('medium')
                high = form1.cleaned_data.get('high')
                vhigh = form1.cleaned_data.get('vhigh')

                tmrt = TMRTParams(
                    user=self.request.user,
                    vlow=vlow,
                    low=low,
                    medium=medium,
                    high=high,
                    vhigh=vhigh
                )

                tmrt.save()

                return redirect('PredApp:prediction')

            if form2.is_valid():
                hot = form2.cleaned_data.get('hot')
                warm = form2.cleaned_data.get('warm')
                slwarm = form2.cleaned_data.get('slwarm')
                neutral = form2.cleaned_data.get('neutral')
                slcool = form2.cleaned_data.get('slcool')
                cool = form2.cleaned_data.get('cool')
                cold = form2.cleaned_data.get('cold')

                pmv = PMVParams(
                    user=self.request.user,
                    hot=hot,
                    warm=warm,
                    slwarm=slwarm,
                    neutral=neutral,
                    slcool=slcool,
                    cool=cool,
                    cold=cold
                )

                pmv.save()

                return redirect('PredApp:prediction')

            if form3.is_valid():
                vcold = form3.cleaned_data.get('vcold')
                petcold = form3.cleaned_data.get('petcold')
                petcool = form3.cleaned_data.get('petcool')
                petslcool = form3.cleaned_data.get('petslcool')
                comfort = form3.cleaned_data.get('comfort')
                petslwarm = form3.cleaned_data.get('petslwarm')
                petwarm = form3.cleaned_data.get('petwarm')
                pethot = form3.cleaned_data.get('pethot')
                vhot = form3.cleaned_data.get('vhot')

                pet = PETParams(
                    user=self.request.user,
                    vcold=vcold,
                    cold=petcold,
                    cool=petcool,
                    slcool=petslcool,
                    comfort=comfort,
                    slwarm=petslwarm,
                    warm=petwarm,
                    hot=pethot,
                    vhot=vhot
                )

                pet.save()

                return redirect('PredApp:prediction')

            else:
                return redirect('PredApp:settings')
