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

    return f'card/{instance.first_name}_{instance.last_name}.png'


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
    foto = models.ImageField(upload_to='card/', blank=True, null=True, validators=[
                             FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    over_all = models.IntegerField(editable=False, null=True)

    def calcular_overall(self):
        # Definição dos pesos para cada posição
        pesos = {
            "GK": {"defesa": 0.5, "passe": 0.1, "habilidade": 0.1, "chute": 0.05, "duelo": 0.1, "fisico": 0.15},
            "MEI": {"defesa": 0.1, "passe": 0.3, "habilidade": 0.3, "chute": 0.2, "duelo": 0.05, "fisico": 0.05},
            "ATA": {"defesa": 0.05, "passe": 0.05, "habilidade": 0.1, "chute": 0.5, "duelo": 0.2, "fisico": 0.1},
            "DEF": {"defesa": 0.45, "passe": 0.05, "habilidade": 0.05, "chute": 0.05, "duelo": 0.2, "fisico": 0.2},
        }

        # Pegando os pesos da posição informada
        peso = pesos.get(self.posicao, {})

        # Calculando o Overall com base nos pesos
        overall = (
            (self.defesa * peso.get("defesa", 0)) +
            (self.passe * peso.get("passe", 0)) +
            (self.habilidade * peso.get("habilidade", 0)) +
            (self.chute * peso.get("chute", 0)) +
            (self.duelo * peso.get("duelo", 0)) +
            (self.fisico * peso.get("fisico", 0))
        )

        return round(overall, 2)

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Verifica se é um novo objeto
        self.over_all = self.calcular_overall()
        # Primeiro salva o objeto para garantir que ele tenha um `pk`
        super().save(*args, **kwargs)
        # Agora que o objeto tem um `pk`, verificamos se a imagem precisa ser renomeada
        new_filename = f'{self.pk}-{self.first_name}_{self.last_name}.png'
        os.rename(self.foto.path, f'media/card/{new_filename}')
        super().save(*args, **kwargs)  # Salva novamente com o nome correto
        self.foto.name = f'card/{new_filename}'
        super().save(*args, **kwargs)  # Salva novamente com o nome correto

        # Agora a imagem já existe no disco, então podemos processá-la
        if is_new and self.foto and os.path.exists(self.foto.path):
            remove_background(self.foto.path, self.foto.path)

    def __str__(self):
        return self.first_name
