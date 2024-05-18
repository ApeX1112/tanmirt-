from django.urls import path
from .views import home,register,loginUser,LogoutUser,Post_on_Tanmirt,showitem
from .views import TanmirtMessage , UserProfileView,TanmirtInbox

urlpatterns = [
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/',loginUser,name='login'),
    path('logout/',LogoutUser,name='logout'),
    path('myposts',Post_on_Tanmirt,name='myposts'),

    path('item/<str:pk>/',showitem,name='item'),
    path('message/<str:userid>',TanmirtMessage,name='message'),
    path('profile/<str:userid>',UserProfileView,name='profile'),
    path('inbox',TanmirtInbox,name='inbox')
]