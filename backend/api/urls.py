from django.urls import path
from .views import home,register,loginUser,LogoutUser,Post_on_Tanmirt,showitem

urlpatterns = [
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/',loginUser,name='login'),
    path('logout/',LogoutUser,name='logout'),
    path('myposts',Post_on_Tanmirt,name='myposts'),

    path('item/<str:pk>/',showitem,name='item')
]