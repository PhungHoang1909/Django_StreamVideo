from django.urls import path
from .views import home, group_detail, delete_stream

urlpatterns = [
    path('', home, name='home'),
    path('group/<int:pk>/', group_detail, name='group_detail'),
    path('stream/<int:pk>/delete/', delete_stream, name='delete_stream'),
]
