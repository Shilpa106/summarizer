from django.db import models



class Feature(models.Model):
    title        = models.CharField(max_length=100)
    total_pages = models.IntegerField(default=0)
    word_count  = models.IntegerField(default=0)
    image_count = models.IntegerField(default=0)
    etc         = models.CharField(max_length=100)
    


    def __str__(self):
        return self.name
