from django.db import models




class UploadFiles(models.Model):
    upload_file         = models.FileField(upload_to='files/')
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Upload Files'
        verbose_name_plural = 'Upload Files'

    def __str__(self):
        return str(self.upload_file.name)
