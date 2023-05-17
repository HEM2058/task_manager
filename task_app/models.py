from django.db import models
from osgeo import gdal
from django.contrib.gis.db import models
# Create your models here.




class User(models.Model):
    name = models.CharField(max_length=50)
    email  = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    

    
    



class DrawnFeature(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    feature_type = models.CharField(max_length=50)
    feature = models.GeometryField()
