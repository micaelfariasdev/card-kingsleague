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
    ('GK','Goleiro'),
    ('MEI','Meio-Campo'),
    ('ATA','Atacante'),
    ('DEF','Defensor'),
]

def path_and_rename(instance, filename):
    """
    Função para gerar o caminho dinâmico do arquivo baseado no campo 'name'
    """
    _, file_extension = os.path.splitext(filename)
    cam = f'card/{instance.pk}-{instance.first_name}_{instance.last_name}{file_extension}'
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

    def save(self, *args, **kwargs):
        # Chama o método save do modelo para garantir que a foto seja salva primeiro
        super().save(*args, **kwargs)

        # Se houver uma foto, remove o fundo e sobrescreve a imagem
        if self.foto:
            # Caminho para o arquivo temporário
            input_image_path = self.foto.path
            output_image_path = input_image_path  # Sobrescreve a imagem original

            # Chama a função de remoção de fundo
            remove_background(input_image_path, output_image_path)

        super().save(*args, **kwargs)


    def __str__(self):
        return self.first_name