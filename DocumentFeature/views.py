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
from DocumentFeature import features
import json

"""
FeaturesList
    - Prepares the list of features yet to shift into database
"""
class FeaturesList(APIView):
    def get(self, request, format=None):
        # features = [
        #     {"id": 1, "name": "Title Name"},
        #     {"id": 2, "name": "Total no of Pages"},
        #     {"id": 3, "name": "Total Word Count"},
        #     {"id": 4, "name": "Total Images"},
        #     {"id": 5, "name": "Content"},
        #     {"id": 6, "name": "Total Paragraphs"},
        #     {"id": 7, "name": "Lookup Word"},   
        #     {"id": 8, "name": "Another One"}, 
        # ]
        feature = features.get_features()
        # print(feature)
        
        return Response({'features_list': feature}, status=status.HTTP_200_OK)

"""
FeatureView
    - returns back the value based on the selected feature
"""
class FeatureView(APIView):
    
    def get(self, request, id, doc_id, format=None):
        # try:
        #     feature = Feature.objects.get(id=id)
        #     print(feature)
        # except Exception as e:
        #     print(e)
        #     return Response({'Info': 'No Feature with this id'})
        # try:
            # extracts the extension out of the file type 
        docs = UploadFiles.objects.get(id=doc_id)
        docs_file = (docs.upload_file.url).strip("'")
        docs_file = docs_file.lstrip("/")

        title = None
        for feature in features.get_features():
            print(feature) 
            if feature['id'] == id:
                title = feature['name']
                break

        print("Title : " , title)
                
        if docs_file.endswith(".pdf"):
            content = ContentReader(docs_file, id, title )
            # print(content)
            return Response(content)
        else:
            return Response({'Info': 'Not a PDF document type', 'status': False})
        # except Exception as e:
        #     return Response({"Info": "Document does not exist with this id"})
        # # import pdb; pdb.set_trace()
        
