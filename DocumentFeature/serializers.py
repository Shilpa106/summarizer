from .models import Feature

from rest_framework import serializers


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


# class FeatureViewSerializer(serializers.Serializer):
#     feature_id = serializers.IntegerField()
#     document_id = serializers.IntegerField()

#     class Meta:
#         fields = ['feature_id', 'document_id']
