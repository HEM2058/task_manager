from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin,GeoModelAdmin,GISModelAdmin
from .models import DrawnFeature
from .models import *



class Useradmin(admin.ModelAdmin):
    list_display = ['id', 'name']
admin.site.register(User,Useradmin)

@admin.register(DrawnFeature)
class DrawnFeatureAdmin(OSMGeoAdmin):
    list_display = ['id', 'feature_type']

@admin.register(AssignedPolygon)
class AssignedPolygonAdmin(OSMGeoAdmin):
    list_display = ['id', 'assigned_user']