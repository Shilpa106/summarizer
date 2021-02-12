from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UploadFiles(models.Model):
    user_id             = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name           = models.CharField(max_length=255, null=True, blank=True, default='')
    file_type           = models.CharField(max_length=20, null=True, blank=True, default='')
    upload_file         = models.FileField(upload_to='files/')
    file_size           = models.DecimalField(default=0, decimal_places=2, max_digits=15)
    metadata            = models.TextField(null=True, blank=True)
    category            = models.CharField(max_length=100, default='Unknown')
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Upload Files'
        verbose_name_plural = 'Upload Files'

    def __str__(self):
        return self.file_name or self.file_type + " by " + str(self.user_id.username)
