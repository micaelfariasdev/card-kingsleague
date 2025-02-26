from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import os
from .utils import remove_background

times = [
    ('capim_fc', 'Capim FC'),
    ('dendele', 'Dendele'),
    ('desimpedidos_goti', 'Desimpedidos Goti'),
    ('fluxo', 'Fluxo FC'),
    ('funkbol', 'Funkbol'),
    ('furia', 'Furia FC'),
    ('g3x', 'G3X'),
    ('loud', 'Loud SC'),
    ('nyvelados', 'Nyvelados'),
    ('real_elite', 'Real Elite'),
]

pos = [
    ('GK', 'Goleiro'),
    ('MEI', 'Meio-Campo'),
    ('ATA', 'Atacante'),
    ('DEF', 'Defensor'),
]


def path_and_rename(instance):
    """
    Função para gerar o caminho dinâmico do arquivo baseado no campo 'name'
    """
    cam = f'card/{instance.pk}-{instance.first_name}_{instance.last_name}.png'
    return cam


class CardCreate(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    time = models.CharField(max_length=50, choices=times)
    posicao = models.CharField(max_length=50, choices=pos)
    defesa = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ])
    passe = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ])
    habilidade = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ])
    chute = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ])
    duelo = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ])
    fisico = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ])
    foto = models.ImageField(upload_to=path_and_rename, blank=True, null=True)
    over_all = models.IntegerField(editable=False)

    def over_all_mid(self):
        atributos = [self.defesa, self.passe, self.habilidade,
                     self.chute, self.duelo, self.fisico]
        return int(sum(atributos) / len(atributos))

    def save(self, *args, **kwargs):
        
        is_new = self.pk is None  

        super().save(*args, **kwargs)  

        self.over_all = self.over_all_mid()
        super().save(*args, **kwargs)  

        if is_new and self.foto:
            input_image_path = self.foto.path
            output_image_path = input_image_path  
            remove_background(input_image_path, output_image_path)


    def __str__(self):
        return self.first_name
