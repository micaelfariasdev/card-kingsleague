from django.urls import path
from cards import views

app_name = 'cards'

urlpatterns = [
    path('', views.home, name='home'),
    path('view/<int:id>', views.view, name='view-detail')
]
