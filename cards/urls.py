from django.urls import path
from . import views


app_name = 'cards'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('view/<int:id>', views.view, name='view-detail')
]
