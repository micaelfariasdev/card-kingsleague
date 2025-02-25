import os
import cv2
import numpy as np
import rembg
from django.db import models
from django.core.files.base import ContentFile
from PIL import Image
import io
from django.core.validators import MinValueValidator, MaxValueValidator


face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def processar_imagem(imagem):
    """Detecta rosto, recorta para centralizar e remove o fundo."""
    img = np.array(imagem)  # Converte para array do OpenCV
    # Converte para escala de cinza
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detecta rostos
    rostos = face_cascade.detectMultiScale(
        cinza, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

    if len(rostos) == 0:
        return None  # Nenhum rosto detectado

    # Pega o primeiro rosto detectado
    x, y, w, h = rostos[0]

    # Expande a área do rosto para melhor enquadramento
    margem = int(0.4 * w)  # Ajuste para capturar um pouco do pescoço
    x1, y1 = max(0, x - margem), max(0, y - margem)
    x2, y2 = min(img.shape[1], x + w +
                 margem), min(img.shape[0], y + h + margem)

    # Recorta e redimensiona para um tamanho fixo
    rosto_recortado = img[y1:y2, x1:x2]
    rosto_recortado = cv2.resize(rosto_recortado, (500, 500))

    # Remove o fundo usando rembg
    img_pil = Image.fromarray(cv2.cvtColor(rosto_recortado, cv2.COLOR_BGR2RGB))
    img_sem_fundo = rembg.remove(img_pil)

    return img_sem_fundo


def renomear_imagem(instance, filename):
    ext = filename.split('.')[-1]  # Obtém a extensão do arquivo
    nome_formatado = str(instance.name).lower().replace(
        " ", "_")  # Formata o nome

    if instance.pk:
        # nomePessoa_id.ext
        novo_nome = f"{nome_formatado}_{instance.pk}.{ext}"
    else:
        novo_nome = f"{nome_formatado}.{ext}"  # Caso o ID ainda não exista

    return os.path.join('card/', novo_nome)


class CardCreate(models.Model):
    name = models.IntegerField(max_length=2, validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ])
    time = models.CharField(choices=times)
    posicao = models.CharField(choices=pos)
    defesa = models.IntegerField(max_length=2, validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ])
    passe = models.IntegerField(max_length=2, validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ])
    habilidade = models.IntegerField(max_length=2, validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ])
    chute = models.IntegerField(max_length=2, validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ])
    duelo = models.IntegerField(max_length=2, validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ])
    fisico = models.IntegerField(max_length=2, validators=[
        MinValueValidator(0),
        MaxValueValidator(99)
    ])
    foto = models.ImageField(upload_to='card/', blank=True, null=True)

    def save(self, *args, **kwargs):
        """Ao salvar, processa a imagem e salva com o nome 'nome_id.png'."""
        super().save(*args, **kwargs)  # Salva primeiro para gerar o ID

        if self.foto:
            # Abrir a imagem original
            foto_aberta = Image.open(self.foto).convert("RGB")
            img_processada = processar_imagem(foto_aberta)

            if img_processada:
                # Renomeia a imagem para 'nome_id.png'
                novo_nome = f"card/{self.name.lower().replace(' ', '_')}_{self.pk}.png"

                # Converte a imagem para bytes e salva
                img_io = io.BytesIO()
                img_processada.save(img_io, format="PNG")
                self.foto.save(novo_nome, ContentFile(
                    img_io.getvalue()), save=False)

        super().save(*args, **kwargs)  # Salva novamente com a imagem processada

    def __str__(self):
        return self.name
