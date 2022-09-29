from django.conf import settings
from django.db import models

from PIL import Image

class Photo(models.Model):
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    #on definit une fonction qui va reduire la taille des photos
    IMAGE_SIZE = (800, 800)
    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_SIZE)
        image.save(self.image.path)

    #on surcharge de la fonction save pour que lorsqu'elle est utilisé pour enregistrer une 
    #une image elle la réduise directement
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image() #on ajout à la méthode save la méthode pour reduire la taille des photos


class Blog(models.Model):
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    word_count = models.IntegerField(null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)

    #fonction pour compter le nombre de caractères dans le contenu
    def _get_word_count(self):
        return len(self.content.split(' '))

    #on surcharge la fonction save pour qu'elle enregistre automatiquement le nombre de mots dans la variable word_count
    def save(self, *args, **kwargs):
        self.word_count = self._get_word_count()
        super().save(*args, **kwargs)