from django.db import models


'''
    Feature List:
        title name
        total number of pages
        total word count
        total images
        content
        total paragraphs
        lookup word
'''


class Feature(models.Model):
    name        = models.CharField(max_length=100)
    


    def __str__(self):
        return self.name
