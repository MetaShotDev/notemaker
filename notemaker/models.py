from django.db import models


class NoteMakerModel(models.Model):
    youtubeLink = models.CharField(max_length=100)
    processing = models.CharField(max_length=100)
    noteType = models.CharField(max_length=100)
    noteDoc = models.FileField(upload_to='notes/', null=True, blank=True)

    def __str__(self):
        return self.youtubeLink
