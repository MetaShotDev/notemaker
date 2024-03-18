from django.db import models


class NoteMakerModel(models.Model):
    youtubeLink = models.CharField(max_length=100)
    processing = models.CharField(max_length=100)
    noteType = models.CharField(max_length=100)
   

    def __str__(self):
        return self.youtubeLink
