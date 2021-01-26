from django.urls import path
from web_trial.views import employeeList
from . import views

urlpatterns = [
    path('', employeeList.as_view()),
    # path('', views.abcd, name="abcd"),
]
