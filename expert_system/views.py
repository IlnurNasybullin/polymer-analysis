from http.client import OK
from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout

from expert_system.calculation.CalculationResult import CalculationAdapter
from .models import Result
import json

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
        image_data = float(data["umPerPixel"])
        comment = data["comment"]
        jsn = "{ \"all polymers count\": " + str(all_polymers_count) + ", " + "\" disp polymers count\" :" + str(disp_polymers_count) + ", " +  "\" umPerPixels\" :" + str(image_data)+" }"        

        resul = Result.objects.create_result(str(comment), str(email), str(image_data), jsn, str(mean_value))
        resul.save()

        return JsonResponse({})

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
