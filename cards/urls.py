from django.urls import path

app_name = 'cards'

urlpatterns = [
    path('', views.home, name='home')
]
