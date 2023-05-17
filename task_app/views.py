from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def Index(request):
    return render(request,'index.html')
def LoginPage(request):
    return render(request,'login.html')
def Login(request):
     if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            Tuser = User.objects.get(email=email)
        except ObjectDoesNotExist:
            msg = "User with this email address does not exist"
            return render(request, 'login.html', {'msg': msg})

        if Tuser.password == password:
            request.session['id'] = Tuser.id
            msg = f"Welcome {Tuser.name}! You have successfully logged in as Mapper"
            return render(request, 'index.html', {'msg': msg})
        else:
            msg = "Please enter a valid password"
            return render(request, 'login.html', {'msg': msg})

@csrf_exempt
def save_feature(request):
    id = request.session.get('id')
    user = User.objects.get(id=id)
    if request.method == 'POST':
        # decode the byte string into a regular string
        body = request.body.decode('utf-8')
        print("===================================================================")
        print(body)
        # parse the JSON string into a Python object
        data = json.loads(body)
        print("===================================================================")
        print(data)
        # check if the 'features' key exists in the data
        if data and isinstance(data, list):
            for feature in data:
                feature_type = feature['geometry']['type']
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print(feature_type)
                geometry = json.dumps(feature['geometry'])
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print(geometry)
                DrawnFeature.objects.create(feature_type=feature_type, feature=geometry,user=user)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
