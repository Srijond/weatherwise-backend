
from django.urls import path
from .views import compare_temperatures, coolest_districts_view

urlpatterns = [
    path('coolest_districts/', coolest_districts_view, name='coolest_districts'),
    path('compare_temperatures/', compare_temperatures, name='compare_temperatures'),

]
