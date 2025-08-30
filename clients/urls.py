
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginClient, name='LoginClient'),
    path('signup/', views.signup_client, name='SignUpClient'),
    path('afterLogin/',views.afterLogin, name='afterLogin'),
    path('logout/', views.logout_view, name='logout_client'),
]
