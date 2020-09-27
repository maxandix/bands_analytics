from django.db import models

class SearchRequest(models.Model):
    artist_name = models.CharField(max_length=512)
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f'{self.artist_name} (creaded at {self.creation_date})'