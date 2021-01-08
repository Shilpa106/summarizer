from .models import SubscriptionType

from rest_framework import serializers



class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = '__all__'