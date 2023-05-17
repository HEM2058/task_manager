from django.urls import path
from task_app import views

urlpatterns = [
    path('',views.LoginPage,name='loginpage'),
    path('login/',views.Login,name="login"),
    path('home',views.Index,name="index"),
    path('api/save-feature', views.save_feature, name='save_feature'),
]
