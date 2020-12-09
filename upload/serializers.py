from rest_framework import serializers
from . models import UploadFiles


class UploadFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFiles
        fields = '__all__'
