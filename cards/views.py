from django.shortcuts import render, redirect
from .models import CardCreate
from .forms import CardCreateForm


def home(request):
    cards = CardCreate.objects.all().order_by('-id')
    cards_over = CardCreate.objects.all().order_by('-over_all')
    return render(request, 'cards/home.html', {'cards': cards, 'cards_over': cards_over})


def view(request, id):
    card = CardCreate.objects.get(id=id)
    return render(request, 'cards/view-detail.html', {'card': card})


def create(request):
    form = CardCreateForm()
    if request.method == 'POST':
        form = CardCreateForm(request.POST, request.FILES)
        print()
        
            
        if form.is_valid():
            card = form.save()  # Salva o formulário
            # Redireciona para a view do card
            return redirect('cards:view-detail', id=card.pk)
        else:
            print('Formulário não válido')
            # Caso o formulário não seja válido, redireciona de volta
            return redirect('crards:home')
    return render(request, 'cards/create.html', {'form': form})


def viewcard(request, id):
    card = CardCreate.objects.get(id=id)
    return render(request, 'cards/view-card.html', {'card': card})

