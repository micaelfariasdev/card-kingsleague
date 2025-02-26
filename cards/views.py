from django.shortcuts import render
from .models import CardCreate
from .forms import CardCreateForm



def home(request):
    form = CardCreate.objects.all()
    return render(request, 'cards/home.html', {'cards': form, })


def view(request, id):
    card = CardCreate.objects.get(id=id)
    return render(request, 'cards/view-detail.html', {'card':card})

def create(request):
    form = CardCreateForm()
    return render(request, 'cards/create.html', {'form':form})

