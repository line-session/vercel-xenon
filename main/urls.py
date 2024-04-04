from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('handle', views.logout_views, name='logout'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('login', views.login_views, name='login'),
    path('home/show', views.show, name='show'),
    path('home/add', views.add, name='add'),
    path('home/delete', views.delete, name='delete'),
    path('home/change', views.change, name='change'),
    path('home/sell', views.sell, name='sell'),
]