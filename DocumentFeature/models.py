from django.db import models
from DocumentUpload.models import UploadFiles


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


class ResultFeature(models.Model):
    docs_id     = models.ForeignKey(UploadFiles, on_delete=models.CASCADE)
    body        = models.TextField()

    def __str__(self):
        return self.docs_id.file_type

class FeatureList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name