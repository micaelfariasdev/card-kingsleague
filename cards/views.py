from django.shortcuts import render, redirect
from .models import CardCreate
from .forms import CardCreateForm


def home(request):
    form = CardCreate.objects.all().order_by('-id')
    return render(request, 'cards/home.html', {'cards': form, })


def view(request, id):
    card = CardCreate.objects.get(id=id)
    return render(request, 'cards/view-detail.html', {'card': card})


def create(request):
    form = CardCreateForm()
    if request.method == 'POST':
        form = CardCreateForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save()  # Salva o formulário
            # Redireciona para a view do card
            return redirect('cards:view-detail', id=card.pk)
        else:
            print('Formulário não válido')
            # Caso o formulário não seja válido, redireciona de volta
            return redirect('create')
    return render(request, 'cards/create.html', {'form': form})



