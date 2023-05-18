from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def Index(request):
    id = request.session.get('id')
    user = User.objects.get(id=id)
    try:
      assigned_polygon = AssignedPolygon.objects.get(assigned_user=user)  # Replace with the appropriate query to retrieve the desired polygon
    except ObjectDoesNotExist:
        return render(request,'index.html')
    
    
    if assigned_polygon.polygon:
        polygon_center = assigned_polygon.polygon.centroid
        # Access the center coordinates
        center_latitude = polygon_center.y
        center_longitude = polygon_center.x
        polygon =  assigned_polygon.polygon
        print("===============================================================")
        print(center_latitude, center_longitude)
        return render(request,'index.html',{'lat':center_latitude,'lng':center_longitude,'polygon':polygon})
    else:
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
            return redirect('index')
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
