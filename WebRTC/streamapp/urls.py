from django.urls import path
from .views import main_view

urlpatterns = [
    # Call function main_view to return base.html
    path('', main_view, name='main_view'),
]
