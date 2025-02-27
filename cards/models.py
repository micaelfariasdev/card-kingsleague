from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
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


def path_and_rename(instance, filename):
    """
    Função para gerar o caminho dinâmico do arquivo baseado no campo 'name'
    """
  
    return f'card/{instance.pk}-{instance.first_name}_{instance.last_name}.png'


class CardCreate(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    time = models.CharField(max_length=50, choices=times, default=times[0])
    posicao = models.CharField(max_length=50, choices=pos, default=pos[0])
    defesa = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ], default=50)
    passe = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ], default=50)
    habilidade = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ], default=50)
    chute = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ], default=50)
    duelo = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ], default=50)
    fisico = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ], default=50)
    foto = models.ImageField(upload_to=path_and_rename, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    over_all = models.IntegerField(editable=False, null=True)

    def over_all_mid(self):
        atributos = [self.defesa, self.passe, self.habilidade,
                     self.chute, self.duelo, self.fisico]
        return int(sum(atributos) / len(atributos))

    def save(self, *args, **kwargs):
    # Verificar se é um novo objeto
        is_new = self.pk is None

        # Calcular o over_all
        self.over_all = self.over_all_mid()

        # Salvar o objeto com o over_all calculado
        super().save(*args, **kwargs)

        # Se for um novo objeto e houver foto, remova o fundo
        if is_new and self.foto:
            input_image_path = self.foto.path
            output_image_path = input_image_path  # Aqui você pode alterar para salvar em outro diretório se necessário
            remove_background(input_image_path, output_image_path)


    def __str__(self):
        return self.first_name
