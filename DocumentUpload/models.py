from django.db import models
from django.contrib.auth import get_user_model

from DocumentFeature.models import Feature

User = get_user_model()




class UploadFiles(models.Model):
    user_id             = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name           = models.CharField(max_length=255, null=True, blank=True, default='')
    file_type           = models.CharField(max_length=20, null=True, blank=True, default='')
    upload_file         = models.FileField(upload_to='files/')
    file_size           = models.FloatField(default=0)
    metadata            = models.TextField(null=True, blank=True)
    category            = models.CharField(max_length=100, default='Unknown')
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Upload Files'
        verbose_name_plural = 'Upload Files'

    def __str__(self):
        return str(self.upload_file.name)



class DocumentFeature(models.Model):
    name = models.CharField(max_length=100)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)


    def __str__(Self):
        return Self.name