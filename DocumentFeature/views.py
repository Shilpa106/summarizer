from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializers import FeatureSerializer
from .models import Feature
from DocumentUpload.models import UploadFiles

from .services.ocrContentReader import ContentReader

import os


# class FeaturesList(generics.ListAPIView):
#     queryset = Feature.objects.all()
#     serializer_class = FeatureSerializer


#     def get(self, request, format=None):
#         all_feature = self.get_queryset()
#         serializer = self.serializer_class(all_feature, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class FeaturesList(APIView):
    def get(self, request, format=None):
        features = [
            {"id": 1, "name": "Title Name"},
            {"id": 2, "name": "Total no of Pages"},
            {"id": 3, "name": "Total Word Count"},
            {"id": 4, "name": "Total Images"},
            {"id": 5, "name": "Content"},
            {"id": 6, "name": "Total Paragraphs"},
            {"id": 7, "name": "Lookup Word"},   
        ]
        
        return Response({'features_list': features}, status=status.HTTP_200_OK)


class FeatureView(APIView):
    
    def get(self, request, id, doc_id, format=None):
        # try:
        #     feature = Feature.objects.get(id=id)
        #     print(feature)
        # except Exception as e:
        #     print(e)
        #     return Response({'Info': 'No Feature with this id'})
        docs = UploadFiles.objects.get(id=doc_id)
        docs_file = (docs.upload_file.url).strip("'")
        docs_file = docs_file.lstrip("/")
        if docs_file.endswith(".pdf"):
            content = ContentReader(docs_file, id)
            # print(content)
            return Response(content)
        else:
            return Response({'Info': 'Not a PDF document type', 'status': False})
        # import pdb; pdb.set_trace()
        
