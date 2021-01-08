from rest_framework import serializers
from . models import UploadFiles


class UploadFilesSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = UploadFiles
        fields = '__all__'
