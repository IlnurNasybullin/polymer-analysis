from http.client import OK
from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout

from expert_system.calculation.CalculationResult import CalculationAdapter
from .models import Result
import json
from pathlib import Path
import datetime

from base64 import b64decode

SAVE_DIR = '.polymer-analysis'

# TODO: save data (with current date)!
def index(request):
    if request.method == "GET":
        return render(request, 'index.html')

def save(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data["email"]
        all_polymers_count = int(data["allPolymersCount"])
        disp_polymers_count = int(data["dispPolymersCount"])
        mean_value = float(data["meanValue"])
        um_per_pixel = float(data["umPerPixel"])
        comment = data["comment"]
        img_base64 = data["prImage"]
        min_disp = int(data["minDisp"])
        max_disp = int(data["maxDisp"])
        temperature = int(data["temperature"])

        now = datetime.datetime.now(datetime.timezone.utc)
        filename = f'prediction-image-{now.strftime("%Y-%m-%dT%H%M%S")}.png'

        img_url = save_img(img_base64, filename)

        jsn_dict = {
            "allPolymersCount": all_polymers_count,
            "dispPolymersCount": disp_polymers_count,
            "umPerPixel": um_per_pixel,
            "minDisp": min_disp,
            "maxDisp": max_disp,
            "temperature": temperature
        }

        jsn = json.dumps(jsn_dict)

        resul = Result.objects.create_result(str(comment), now, str(email), str(um_per_pixel), jsn, str(mean_value), uri=img_url)
        resul.save()

        return JsonResponse({})

def save_img(img_base64: str, filename: str):
    dir = Path.home() / SAVE_DIR
    dir.mkdir(exist_ok=True)

    fdir = dir / filename

    with open(fdir, 'wb') as f:
        f.write(b64decode(img_base64))

    return fdir.as_uri()

def history(request):
    results = Result.objects.all()
    return render(request, 'history.html', {'results': results})

def calculate(request):
    if request.method == 'POST':
        um_per_pixel = request.POST["umPerPixel"]
        temperature = request.POST["temperature"]
        min_disp = request.POST["minDisp"]
        max_disp = request.POST["maxDisp"]
        image_bytes = request.FILES["image"].read()
        
        args = {
            'image_bytes': image_bytes, 
            'um_per_pixel': um_per_pixel, 
            'temperature': temperature, 
            'min_disp': min_disp, 
            'max_disp': max_disp
            }

        res = CalculationAdapter.to_calculation(args).to_result()

        return JsonResponse(res)

def logout_view(request):
    logout(request)
    return redirect('/login')
