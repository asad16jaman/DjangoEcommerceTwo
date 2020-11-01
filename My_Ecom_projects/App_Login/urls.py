from django.urls import path
from . import views



app_name='app_login'

urlpatterns=[
    path('signup',views.sign_up,name='singup_page'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('profile/',views.create_Profile,name='profile'),
]