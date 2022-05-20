from django.urls import path
from . import views

urlpatterns = [ path('',views.index), path('brown_misses_cony',views.brown) ]