from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from .serializers import SubscriptionTypeSerializer
from .models import SubscriptionType



class SubscriptionTypeView(generics.ListCreateAPIView):
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeSerializer
    lookup_field = 'id'


class SubscriptionTypeDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeSerializer
    lookup_field = 'id'






