from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class FeaturesList(APIView):

    def get(self, request, format=None):
        features = [
            {'id': '1', 'name': 'Title Name'},
            {'id': '2', 'name': 'Total No of Pages'},
            {'id': '3', 'name': 'Total Word Count'},
            {'id': '4', 'name': 'Total Images'},
            {'id': '5', 'name': 'Etc'}
        ]

        return Response({'features_list': features}, status=status.HTTP_200_OK)



class FeatureView(APIView):

    def get(self, request, id, format=None):
        if id == 1:
            return Response({'Title Name': 'Docs about share market....'})
        elif id == 2:
            return Response({'Total No of Pages': 25})
        elif id == 3:
            return Response({'Total Word Count': 500})
        elif id == 4:
            return Response({'Total Images': 4})
        else:
            return Response({'Etc': 'Etc'})