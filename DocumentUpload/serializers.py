from rest_framework import serializers
from . models import UploadFiles


class UploadFilesSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = UploadFiles
        # fields = '__all__'
        exclude = ('updated_at', 'created_at')
        extra_kwargs = {'category': {'read_only': True},
                        'file_type': {'read_only': True},
                        'file_size': {'read_only': True},
                        'metadata': {'read_only': True},}